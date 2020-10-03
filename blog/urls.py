from django.contrib import admin
from django.urls import path, include
from . import views
from .views import BlogPostUpdateView

urlpatterns = [
    path('',views.bloghome,name='bloghome'),
    path('/createblog',views.createblog,name='createblog'),
    path('/saveblog',views.saveblog,name='saveblog'),
    path('/postcomment',views.PostComment,name='postcomment'),
    path('/Blogsearch',views.Blogsearch,name='Blogsearch'),
    path('/userblogposts',views.userblogposts,name='userblogposts'),
    path('/deleteblogpost',views.deleteblogpost,name='deleteblogpost'),
    path('/deletethepost',views.deletethepost,name='deletethepost'),
    path('/<str:slug>/update',BlogPostUpdateView.as_view(),name='blogpost-update'),
    path('/<str:slug>',views.blogpostview,name='blogpostview'),
]