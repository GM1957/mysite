from django import forms 
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from listofposts.models import Post
from . models import Product
# creating a form  
class ContentInputForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'titile here...',
            
        }
    ))
    parentname = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'hint: checkout the home page if not there then add a new one...',
            
        }
    ))
   
    class Meta:
        model = Post
        fields = [
            'title',
            'parentname',
            'content',
        ]
    
   # Add_Content = forms.CharField(widget=CKEditorUploadingWidget())

# class ContentInputForm(forms.Form):
#     Add_content = forms.CharField(widget=CKEditorUploadingWidget())   
 

class ProductAddForm(forms.Form): 
    product_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control mb-3',
            'placeholder':'Choose an unique name which is not already present and must be under 100 Characters! '
        }
    )) 
    description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'form-control mb-3',
            'placeholder':'Try to give a short description under 300 characters!'
        }
    )) 

