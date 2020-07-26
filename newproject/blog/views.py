from django.shortcuts import render,redirect,reverse , get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from blog.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView)
from .models import Post,Comment
from django.utils import timezone
from .forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



#class based views
class PostListView(ListView):
    template_name='post_list.html'
    model=Post
    def get_queryset(self):
        return Post.objects.filter(publish_date__lte= timezone.now()).order_by('-publish_date')


class PostDetailView(DetailView):
    template_name='post_detail.html'
    model= Post


class CreatePostView(LoginRequiredMixin,CreateView):

    redirect_field_name= 'post_detail.html'
    template_name='post_form.html'
    form_class=PostForm
    model= Post

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.author = self.request.user
        self.object.save()
        return redirect('post_list',)

class PostUpdateView(LoginRequiredMixin,UpdateView):
    redirect_field_name= 'detail.html'
    template_name= 'post_form.html'
    form_class=PostForm
    model= Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    template_name= 'post_confirm_delete.html'
    model=Post
    success_url=reverse_lazy('post_list')

class PostDraftList(LoginRequiredMixin,ListView):
    template_name='post_draft_list.html'
    model= Post
    def get_queryset(self):
        # print(self.request.user)
        if 'tonmoy' in str(self.request.user):
            return Post.objects.filter(publish_date__isnull=True).order_by('-publish_date')
        else:
            author= User.objects.get(username= self.request.user)
            return Post.objects.filter(publish_date__isnull=True).filter(author= author).order_by('-publish_date')

#################################### All def function 
@login_required
def Dashboard(request):
    draft_post= Post.objects.filter(publish_date__isnull=True).order_by('-publish_date')
    comments= Comment.objects.filter(approved_comment = False).order_by('-created_date')

    context={
        'posts' : draft_post,
        'comments': comments
    }
    return render(request,'dash.html',context)







@login_required
def post_publish(request,pk):
    post= get_object_or_404(Post, pk=pk)
    print("hello ",post.title)
    post.publish
    return redirect('post_detail', pk=pk)


@login_required
def add_new__comment_to_post(request,pk):
    post= get_object_or_404(Post,pk=pk)
    author= User.objects.get(username= request.user)
    text= request.POST.get('text')
    comment= Comment(post=post, author=author, text=text)
    comment.save()
    return redirect('post_detail', pk=pk)



@login_required
def add_comment_to_post(request, pk):
    post= get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form= CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post= post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form= CommentForm()
    
    context={
        'form': form
    }
    return render(request, 'comment-form.html',context)

@login_required
def comment_approve(request,pk):
    comment= get_object_or_404(Comment, pk=pk)
    print(comment)
    post_pk= comment.post.pk
    comment.approve
    return redirect('post_detail', pk=post_pk)

@login_required
def comment_remove(request,pk):
    comment= get_object_or_404(Comment, pk=pk)
    post_pk= comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

def Home(request):

    posts= Post.objects.filter(publish_date__lte= timezone.now()).order_by('-publish_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)    
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context={
        'posts': posts
    }
    return render(request,'home.html',context)

@login_required
def Profile(request):
    auther= User.objects.get(username= request.user)
    print(auther)
    posts= Post.objects.all().filter(author= auther)
    context= {
        'posts': posts
    }
    return render(request, 'profile.html',context)

@login_required
def UserLogout(request):
    logout(request)
    return redirect('home')

def UserLogin(request):
    if request.method == 'POST':

        username= request.POST.get('username')
        password= request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                print("hello")
                return redirect('home')
            else:
                print("user is not active")
        else:
            messages.error(request,"Username and password are incorrect")

    context={
        'values': request.POST
    }
    print(request.POST)
    return render(request,'login.html', context)

def UserRegister(request):
    
    form=UserForm()
    if request.method == 'POST':
        form= UserForm(request.POST)
        if form.is_valid():
            user= form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request, request.POST['username'] + ' is registered successfully')
            return redirect('login')
        else:
            print("Data is not valid!!!")
    else:
        print("Something wrong")


    context={'form':form}
    return render(request,'register.html',context)