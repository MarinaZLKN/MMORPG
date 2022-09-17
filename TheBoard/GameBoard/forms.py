from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=50, label="Сообщение", widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'type', 'upload']


class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=300, label="Комментарий", widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['text']
