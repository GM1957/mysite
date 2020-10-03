from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.shortcuts import render,HttpResponse,redirect,reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Post(models.Model):
    postsno = models.AutoField(primary_key=True)
    parentname = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    content = RichTextUploadingField(blank=True,null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.CharField(max_length=200)
    timeStamp = models.DateTimeField(null = True,blank=True,default=now)
    
    def __str__(self):
        return self.title + ' by ' + str(self.author)
    def get_absolute_url(self):
        return redirect('/')
        

class Comment(models.Model):
    commentsno = models.AutoField(primary_key = True)
    newcomment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.newcomment[0:20]+'...' + ' -by- ' +str(self.user)
