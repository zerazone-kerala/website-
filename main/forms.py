from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Project

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Username',
        'style': 'padding: 12px; border-radius: 8px; border: 1px solid #ddd; width: 100%; margin_bottom: 10px;'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password',
        'style': 'padding: 12px; border-radius: 8px; border: 1px solid #ddd; width: 100%;'
    }))

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Title',
                'style': 'padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 100%;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Project Description',
                'rows': 4,
                'style': 'padding: 10px; border-radius: 5px; border: 1px solid #ccc; width: 100%;'
            }),
        }
