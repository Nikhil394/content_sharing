from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import UserPost
from .forms import UserPostForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from django.contrib import messages
from .users.forms import CustomUserCreationForm 


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after registration
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('posts/')  # Redirect to a home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



@login_required
def create_post(request):
    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('view_posts')
    else:
        form = UserPostForm()
    return render(request, 'posts/create_post.html', {'form': form})

from django.shortcuts import render
import os
from django.utils import timezone
from django.conf import settings

@login_required
def view_posts(request):
    posts = UserPost.objects.all().order_by('-created_at')
    for post in posts:
        if post.content_file:
            extension = os.path.splitext(post.content_file.name)[1].lower()
            if extension in [".jpg", ".jpeg", ".png", ".gif"]:
                post.file_type = "image"
            elif extension in [".mp4", ".webm", ".ogg", ".mkv"]:
                post.file_type = "video"
            elif extension == ".pdf":
                post.file_type = "pdf"
            else:
                post.file_type = "other"
        else:
            post.file_type = None
        post.created_at = timezone.localtime(post.created_at)
    return render(request, 'posts/view_posts.html', {'posts': posts, 'user': request.user})

@login_required
def user_posts(request):
    posts = UserPost.objects.filter(user=request.user).order_by('-created_at')
    for post in posts:
        if post.content_file:
            extension = os.path.splitext(post.content_file.name)[1].lower()
            if extension in [".jpg", ".jpeg", ".png", ".gif"]:
                post.file_type = "image"
            elif extension in [".mp4", ".webm", ".ogg", ".mkv"]:
                post.file_type = "video"
            elif extension == ".pdf":
                post.file_type = "pdf"
            else:
                post.file_type = "other"
        else:
            post.file_type = None
        post.created_at = timezone.localtime(post.created_at)
    return render(request, 'posts/user_posts.html', {'posts': posts, 'user': request.user})


import os

@login_required
def delete_post(request, pk):
    post = UserPost.objects.get(pk=pk)
    if request.method == 'POST':
        file_path = "C:/Users/nikhi/Desktop/chatapp/content_sharing/media/" + str(post.content_file)
        if(os.path.exists(file_path)):
            os.remove(file_path)
        print(post)
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('view_posts')
    return render(request, 'posts/delete_post.html', {'post': post})

@login_required
def edit_post(request, pk):
    post = UserPost.objects.get(pk=pk)
    if request.method == 'POST':
        form = UserPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('view_posts')
    else:
        form = UserPostForm(instance=post)
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('login')
    return render(request, 'posts/delete_account.html')