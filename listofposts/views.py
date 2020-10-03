from django.shortcuts import render,HttpResponse,redirect
from .models import Post
from home.models import Product
from django.core.paginator import Paginator

# Create your views here.
def listofposts(request):
    query = request.GET.get('query')
    selectedPosts = Post.objects.filter(parentname=query).order_by('-timeStamp')
    paginator = Paginator(selectedPosts, 15)
    # now no need to render selectedPosts now page_obj will work as selected posts
    # context={'selectedPosts':selectedPosts,'query':query}  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={'query':query,'page_obj':page_obj}        

    return render(request,'section/section.html',context)