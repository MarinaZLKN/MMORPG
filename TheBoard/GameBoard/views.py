from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import PostForm
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-datecreation'
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create_edit.html'
    success_url = reverse_lazy('home')

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create_edit.html'
    success_url = reverse_lazy('home')

