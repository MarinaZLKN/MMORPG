from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(min_length=50, label="Сообщение", widget=forms.Textarea)


    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'type', 'upload']