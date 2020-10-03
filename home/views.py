from django.shortcuts import render,HttpResponse,redirect
from . models import Product,Contact,userdata
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from listofposts.models import Post,Comment
from django.core.paginator import Paginator
from .forms import ContentInputForm,ProductAddForm
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from blog.models import BlogPost

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.

def home(request):
    products = Product.objects.all().order_by('-pub_date')
    paginator = Paginator(products, 18)
    # now no need to render products now page_obj will work as selected posts
    # params = {'product': products}
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    params = {'page_obj': page_obj}
    return render(request,'home/home.html',params)

def feed(request):
    allposts = Post.objects.all()
    paginator = Paginator(allposts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'page_obj':page_obj} 
    return render(request,'home/feed.html',context)

@login_required(login_url='/loginsignup')
def addnewfield(request):
    context ={'form':ProductAddForm()} 
    return render(request,'home/addnewproduct.html',context)
    
@login_required(login_url='/loginsignup')
def ProductSave(request):
    form = ProductAddForm(request.POST,request.FILES)
    if form.is_valid():
        product_name = form.cleaned_data.get('product_name')
        productUniquename = product_name
        description = form.cleaned_data.get('description')
        image = request.FILES['image']
        newproduct = Product.objects.create(product_name=product_name,productUniquename=productUniquename,description=description,image=image)
        newproduct.save()
        messages.success(request,'Your field is Added, Thank you for contributing.')
    else:
        messages.error(request,'Please Fill all the fields correctly')
        return redirect('/addnewfield')
        
    return redirect('/')     

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        content = request.POST['content']
        
        if len(name)<3 or len(email)<4 or len(phonenumber)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly ")
        else:
            contact = Contact(name=name,email=email,phonenumber=phonenumber,content=content)
            contact.save()
            messages.success(request,"Your message has been sent successfully")

    return render(request,'home/contact.html')

def search(request):
    searchquery = request.GET['search']
    if len(searchquery)>200:
        allposts = Post.objects.none()
    if len(searchquery)<4:
        allposts = Post.objects.none()
        messages.error(request,'Please enter more than 4 characters')
        redirect('/')
    else:    
        allpoststitle = Post.objects.filter(title__icontains=searchquery)
        allpostscontent = Post.objects.filter(content__icontains=searchquery)
        allposts = allpoststitle.union(allpostscontent)
        paginator = Paginator(allposts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj':page_obj,'search':searchquery}
        return render(request,'home/search.html',context)
    return render(request,'home/search.html')

def handleSignup(request):
    
    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['signupemail']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 25:
            messages.error(request, "User name must be under 25 Characters")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request, "Password do not match")   
            return redirect('/') 
       
        myuser = User.objects.create_user(username=username,email=email,password=pass2)   
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        default = userdata(user=myuser)
        default.save()
        messages.success(request,'Your account has been created Successfully ')
        return redirect('/')
    else:
        return HttpResponse('NOT ALLOWED')   

def handleLogin(request):
    loginusername = request.POST['loginusername']
    loginpass = request.POST['loginpass']
    user = authenticate(username=loginusername,password=loginpass)
    if user is not None:
        login(request,user)
        messages.success(request,"Successfully Logged In ")
        return redirect('/')
    else:
        messages.error(request,"Please Enter the username or password correctly!")
        return redirect('/')    

@login_required(login_url='/loginsignup')
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('/')      

@login_required(login_url='/loginsignup')
def usersettings(request):
    return render(request,'home/usersettings.html')

def post(request,slug):
    post = Post.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(post=post).order_by('-timestamp')
    context = {'post':post,'comments':comments}
    return render(request,'section/post.html',context)

@login_required(login_url='/loginsignup')
def uploaduserimage(request):
    if request.method == 'POST':
        try:
            pic = request.FILES['profilepicture']
            image = userdata(user=request.user,profile_pic=pic)
            image.save()
        except:
            messages.error(request,"Upload Failed!")
            return redirect('/usersettings')

    else:
        return HttpResponse('NOT-ALLOWED')    
    return redirect('/')

@login_required(login_url='/loginsignup')
def PostComment(request):
    if request.method == 'POST':
        comments = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(postsno=postSno)
        comment = Comment(newcomment=comments,post=post,user=user)
        comment.save()
    return redirect(f'/{post.slug}')

@login_required(login_url='/loginsignup')
def AddNewPost(request): 
    context ={'form':ContentInputForm()} 
    return render(request, "section/addpost.html", context)

@login_required(login_url='/loginsignup')
def SavePost(request):
    form = ContentInputForm(request.POST)
    if form.is_valid():
        author = request.user
        title =  request.POST.get('title')
        parentname =  request.POST.get('parentname')
        content =  request.POST.get('content')
        slug = title.replace(" ", "+")
        newpost = Post.objects.create(title=title,content=content,author=author,parentname=parentname,slug=slug)
        newpost.save()
        messages.success(request,'Your post has been added successfully, Thank you for your great effort.')
        
    return redirect('/')

def loginsignup(request):
    return render(request,'home/loginlink.html')

@login_required(login_url='/loginsignup')
def userallposts(request):
    allsolposts = Post.objects.filter(author=request.user)
    paginator = Paginator(allsolposts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'page_obj':page_obj}
    return render(request,'section/userallposts.html',context) 

@login_required(login_url='/loginsignup')
def deletesolpost(request):
    if request.method == 'POST':
        postid = request.POST.get("deletepostid")
        posttitle = Post.objects.filter(postsno=postid).first()
        context = {'deletepostid': postid,'posttitle':posttitle}
        return render(request, 'section/deleteconfirm.html',context)
    else:
        messages.error(request,'ERROR TO DELETE POST')
        return redirect('/')       

@login_required(login_url='/loginsignup')
def deletethepost(request):
    if request.method == 'POST':
        deletepostconfirmed = request.POST.get('deletepostconfirmed')
        Post.objects.filter(postsno = deletepostconfirmed).delete()
        messages.success(request,'Your post has been Deleted')
        return redirect('/')
    else:
        messages.error(request,'ERROR TO DELETE POST')
        return redirect('/')   

class SolPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','parentname','content','slug']
    success_url = '/userallposts'
    login_url = 'loginsignup'
    def form_valid(self, form):
        form.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False        