from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.shortcuts import render,HttpResponse,redirect,reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class BlogPost(models.Model):
    serialnumber = models.AutoField(primary_key=True)
    blogtitle = models.CharField(max_length=255)
    Thumbnail_image = models.ImageField(upload_to="blog/images/blog_thumbnail_images",blank=True)
    blog_des = models.CharField(max_length=500,blank=True)
    blogcontent = RichTextUploadingField(blank=True,null=True)
    writer = models.ForeignKey(User,on_delete=models.CASCADE)
    slug = models.CharField(max_length=200)
    time = models.DateTimeField(null = True,blank=True,default=now)

    def __str__(self):
        return self.blogtitle + ' by ' + str(self.writer)
    def get_absolute_url(self):
        return redirect('/blog')    

class BlogComment(models.Model):
    commentsno = models.AutoField(primary_key = True)
    newcomment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.newcomment) + ' by ' + str(self.user)
          