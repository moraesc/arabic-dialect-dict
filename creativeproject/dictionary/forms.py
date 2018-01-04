from django import forms
from dictionary.models import *
from django.contrib.auth.models import User
import logging

class NameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['author', 'script_word', 'arabeasy_word',
        'part_of_speech', 'english_definition', 'dialect']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'entry', 'content', 'likes']
