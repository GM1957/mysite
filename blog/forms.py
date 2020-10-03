from django import forms 
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import BlogPost


class blogcreateform(forms.ModelForm):
    blogtitle = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Blog title here...',
            
        }
    ))
    blog_des = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Add a short blog description...',
            
        }
    ))
    class Meta:
        model = BlogPost
        fields = [
            'blogtitle',
            'blog_des',
            'blogcontent',
        ]

        