from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "file", "description", "category"]


from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'نظر خود را بنویسید...'})
        }