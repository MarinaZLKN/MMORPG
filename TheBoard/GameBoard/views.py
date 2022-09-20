from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import PostForm, CommentForm
from .models import Post, Comment


class PostList(ListView):
    model = Post
    ordering = '-datecreation'
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post__pk=self.kwargs.get('pk'), is_accepted=True)
        context['form'] = CommentForm()
        return context

    def get_success_url(self, **kwargs):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})



class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('GameBoard.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create_edit.html'
    success_url = reverse_lazy('home')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('GameBoard.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_create_edit.html'
    success_url = reverse_lazy('home')


class IndexView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        context['comments'] = Comment.objects.filter(post__author=self.request.user)
        return context


class MainPage(TemplateView):
    template_name = 'mainpage.html'


class Comments(PermissionRequiredMixin, CreateView):
    permission_required = ('GameBoard.add_comment',)
    form_class = CommentForm
    model = Comment
    template_name = 'post.html'
    context_object_name = 'comments'

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(post=post, author=self.request.user, text='text')
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # если все ок, создаем обьект
                new_comment = comment_form.save(commit=False)
                # привязываем к посту
                new_comment.post = post
                # сохраняем в БД
                new_comment.save()
            else:
                comment_form = CommentForm()
            return render(request,
                          'post.html',
                          {'post': post,
                           'comment': comment,
                           'comment_form': comment_form})










