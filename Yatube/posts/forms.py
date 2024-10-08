from django import forms

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    """Форма создания поста"""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Форма комментария"""
    class Meta:
        model = Comment
        fields = ('text',)
