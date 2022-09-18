from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
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
        context['comments'] = Comment.objects.filter(is_accepted=True)
        context['form'] = CommentForm()
        return context


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


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'mypage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
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
        # список одобренных комментариев
        comments = post.comments.filter(is_accepted=True)
        comment_form = CommentForm(request.POST)
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
                       'comments': comments,
                       'comment_form': comment_form})


