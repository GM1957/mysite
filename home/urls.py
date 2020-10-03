from django.contrib import admin
from django.urls import path, include
from . import views

from .views import SolPostUpdateView


urlpatterns = [
    path('',views.home,name='home'),
    path('listofposts',include('listofposts.urls')),
    path('blog',include('blog.urls')),              
    path('contact',views.contact,name='contact'),    
    path('feed',views.feed,name='feed'),         
    path('search',views.search,name="search"),
    path('signup',views.handleSignup,name='handleLogin'),
    path('login',views.handleLogin,name='handleSignup'),
    path('logout',views.handleLogout,name='handleLogout'),
    path('usersettings',views.usersettings,name='usersettings'),
    path('uploaduserimage',views.uploaduserimage,name='uploaduserimage'),
    path('postcomment',views.PostComment,name='postcomment'),
    path('AddNewPost',views.AddNewPost,name='AddNewPost'),
    path('SavePost',views.SavePost,name='SavePost'),
    path('addnewfield',views.addnewfield,name='addnewfield'),
    path('ProductSave',views.ProductSave,name='ProductSave'),
    path('loginsignup',views.loginsignup,name='loginsignup'),
    path('deletesolpost',views.deletesolpost,name='deletesolpost'),
    path('deletethepost',views.deletethepost,name='deletethepost'),
    path('userallposts',views.userallposts,name='userallposts'),
    path('<str:slug>',views.post,name='post'),
    path('<str:slug>/update/',SolPostUpdateView.as_view(),name='solpost-update'),
]