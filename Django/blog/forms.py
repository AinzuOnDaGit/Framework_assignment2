from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title","description","image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "description": forms.TextInput(attrs={"class": "form-control", "required": True}),
        }