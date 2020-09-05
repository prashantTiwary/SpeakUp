from django import forms
from .models import Post

class textForm(forms.Form):
    post = forms.CharField(label='Post', widget=forms.Textarea)