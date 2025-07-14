from django import forms
from .models import Resource, Comment, Skill, Achievement, Certificate


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "file", "description", "category"]



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'نظر خود را بنویسید...'})
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'مثلاً برنامه‌نویسی پایتون'}),
            'level': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 100}),
        }

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'organization', 'year', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'organization': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'file': forms.FileInput(attrs={'class': 'form-file-input'}),
        }

        