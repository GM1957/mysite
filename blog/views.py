from django.shortcuts import render,HttpResponse,redirect
from .models import BlogPost,BlogComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from . forms import blogcreateform

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
def bloghome(request):
    blogs = BlogPost.objects.all().order_by('-time')
    paginator = Paginator(blogs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context ={'page_obj':page_obj}
    return render(request,'blog/bloghome.html',context)

@login_required(login_url='/loginsignup')
def createblog(request):
    context ={'form':blogcreateform()} 
    return render(request,'blog/blogcreate.html',context)

@login_required(login_url='/loginsignup')
def saveblog(request):
    form = blogcreateform(request.POST,request.FILES)
    if form.is_valid():
        writer = request.user
        blogtitle = request.POST.get('blogtitle')
        slug = blogtitle.replace(" ", "+")
        Thumbnail_image = request.FILES['thumbimage']
        blog_des = request.POST.get('blog_des')
        blogcontent = request.POST.get('blogcontent')
        newblog = BlogPost.objects.create(writer=writer,blogtitle=blogtitle,slug=slug,Thumbnail_image=Thumbnail_image,
        blog_des=blog_des,blogcontent=blogcontent)
        newblog.save()
        messages.success(request,'Your Story Has Been Posted Successfully :)')
    return redirect('/blog')

def blogpostview(request,slug):
    blogpost = BlogPost.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=blogpost).order_by('-timestamp')
    context = {'blogpost': blogpost, 'comments':comments}
    return render(request,'blog/viewblog.html',context)

@login_required(login_url='/loginsignup')
def PostComment(request):
    if request.method == 'POST':
        comments = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = BlogPost.objects.get(serialnumber=postSno)
        comment = BlogComment(newcomment=comments,post=post,user=user)
        comment.save()
    return redirect(f'/{post.slug}')    

def Blogsearch(request):
    searchquery = request.GET['search']
    if len(searchquery)>200:
        allposts = BlogPost.objects.none()
    if len(searchquery)< 4:
        allposts = BlogPost.objects.none()
        messages.error(request,'Please enter more than 4 characters')
        redirect('/')
    else:    
        allpoststitle = BlogPost.objects.filter(blogtitle__icontains=searchquery)
        allpostscontent = BlogPost.objects.filter(blogcontent__icontains=searchquery)
        allposts = allpoststitle.union(allpostscontent)
        paginator = Paginator(allposts, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj':page_obj,'search':searchquery}
        return render(request,'blog/blogsearch.html',context) 
    return render(request,'blog/blogsearch.html')


def userblogposts(request):
    allblogposts = BlogPost.objects.filter(writer=request.user)
    paginator = Paginator(allblogposts, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'page_obj':page_obj}
    return render(request,'blog/userallblogposts.html',context)  


@login_required(login_url='/loginsignup')
def deleteblogpost(request):
    if request.method == 'POST':
        postid = request.POST.get("deletepostid")
        posttitle = BlogPost.objects.filter(serialnumber=postid).first()
        context = {'deletepostid': postid,'posttitle':posttitle}
        return render(request, 'blog/blogdeleteconfirm.html',context)
    else:
        messages.error(request,'ERROR TO DELETE POST')
        return redirect('/blog')       

@login_required(login_url='/loginsignup')
def deletethepost(request):
    if request.method == 'POST':
        deletepostconfirmed = request.POST.get('deletepostconfirmed')
        BlogPost.objects.filter(serialnumber = deletepostconfirmed).delete()
        messages.success(request,'Your post has been Deleted')
        return redirect('/blog')
    else:
        messages.error(request,'ERROR TO DELETE POST')
        return redirect('/blog')                  

class BlogPostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = BlogPost
    fields = ['blogtitle','Thumbnail_image','blog_des','blogcontent','slug','time']
    success_url = '/blog/userblogposts'
    login_url = 'loginsignup'
    def form_valid(self, form):
        form.writer = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.writer:
            return True
        return False                