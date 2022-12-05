from django import forms
from .models import Post, Image


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the post'}),
            #'author': forms.Select(attrs={'class': 'form-control', 'author': 'Title of the post'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'data-role': 'tagsinput', 'placeholder': 'Tags'}),
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Image
        fields = ('image',)