from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView
from .filters import CommentFilter
from .forms import PostForm, CommentForm
from .models import Post, Comment


@login_required
def approve(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.is_accepted = True
        comment.save()
    return HttpResponseRedirect(f'/mypage/')


@login_required
def disapprove(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.is_accepted = False
        comment.save()
    return HttpResponseRedirect(f'/mypage/')


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
        context['comments'] = Comment.objects.filter(post__pk=self.kwargs.get('pk'))
        context['form'] = CommentForm()
        context['date'] = datetime.utcnow()
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

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Comment.objects.filter(post__author=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
        context['comments'] = Comment.objects.filter(post__author=self.request.user).order_by('-date') #, is_accepted=False
        context['allcomments'] = Comment.objects.filter(post__author=self.request.user).order_by('-date')
        context['filterset'] = self.filterset
        return context

    '''def listing(request):
        all_comments = Comment.objects.filter(post__author=request.user).order_by('-date')
        paginator = Paginator(all_comments, 3)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'mypage.html', {'page_obj': page_obj})'''


class MainPage(TemplateView):
    template_name = 'mainpage.html'


class Comments(PermissionRequiredMixin,CreateView):
    permission_required = ('GameBoard.add_comment',)
    form_class = CommentForm
    ordering = '-date'
    model = Comment
    template_name = 'post.html'
    context_object_name = 'comments'

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
            else:
                comment_form = CommentForm()
        return render(request, 'post.html', {'post': post, 'comment': new_comment, 'comment_form': comment_form})


class DeleteComment(DeleteView):
    model = Comment
    template_name = 'delete.html'
    success_url = reverse_lazy('mypage')













