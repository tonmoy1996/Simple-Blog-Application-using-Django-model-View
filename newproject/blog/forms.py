from django import forms
from django.contrib.auth.models import User
from .models import *
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields= ('username','email','password')

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields= ('title','text')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields= ('author', 'text',)
        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea','rows': 10, 'cols':50}),
        }
