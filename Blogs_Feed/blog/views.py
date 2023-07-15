from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

def home(request):
    context={
        'posts': Post.objects.all()
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model=Post 
    template_name='blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    ordering=['-date_posted']
    paginate_by=5#for 1 page 2 posts

class UserPostListView(ListView):
    model=Post 
    template_name='blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name='posts'
    paginate_by=5#for 1 page 2 posts

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):#template created blog/post_detail.html
    model=Post 


class PostCreateView(LoginRequiredMixin,CreateView):#mixin(here for creating new post user must login 1st) is like decorator in function based views but for classes we can't use decoratot
    model=Post 
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)

#UserPassestestMixin  for test_func
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):#mixin(here for creating new post user must login 1st) is like decorator in function based views but for classes we can't use decoratot
    model=Post 
    fields=['title','content']

    def form_valid(self,form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def test_func(self):#other user should not update another user's post
        post=self.get_object()#which post we are updating
        if self.request.user==post.author:#current logined user==post.author?
            return True
        return False
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):#template created blog/post_detail.html
    model=Post 
    success_url='/'#sending to home page
    
    def test_func(self):#other user should not delete another user's post
        post=self.get_object()#which post we are updating
        if self.request.user==post.author:#current logined user==post.author?
            return True
        return False

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

