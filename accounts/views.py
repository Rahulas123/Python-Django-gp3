from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserSignupForm, BlogPostForm
from .models import BlogPost
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserSignupForm

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # You may perform additional actions here before saving the user
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                # Redirect the user based on their role
                if user.is_doctor:
                    return redirect('doctor_dashboard')
                elif user.is_patient:
                    return redirect('patient_dashboard')
                else:
                    # Handle other user types or redirect to a default page
                    return redirect('dashboard')  # Redirect to a default dashboard view
            else:
                # Handle authentication failure
                return redirect('login')  # Redirect to login page with error message
    else:
        form = UserSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_doctor:
                return redirect('doctor_dashboard')
            elif user.is_patient:
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    elif request.user.is_authenticated:
        if request.user.is_doctor:
            return redirect('doctor_dashboard')
        elif request.user.is_patient:
            return redirect('patient_dashboard')
    return render(request, 'accounts/login.html')

def doctor_dashboard(request):
    if request.user.is_authenticated and request.user.is_doctor:
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.author = request.user
                blog_post.save()
                return redirect('doctor_dashboard')
        else:
            form = BlogPostForm()
        blog_posts = BlogPost.objects.filter(author=request.user)
        return render(request, 'accounts/doctor_dashboard.html', {'form': form, 'blog_posts': blog_posts})
    else:
        return redirect('login')

def patient_dashboard(request):
    if request.user.is_authenticated and request.user.is_patient:
        blog_posts = BlogPost.objects.filter(draft=False)
        return render(request, 'accounts/patient_dashboard.html', {'blog_posts': blog_posts})
    else:
        return redirect('login')

def create_blog_post(request):
    if request.user.is_authenticated and request.user.is_doctor:
        if request.method == 'POST':
            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                blog_post = form.save(commit=False)
                blog_post.author = request.user
                blog_post.save()
                return redirect('doctor_dashboard')
        else:
            form = BlogPostForm()
        return render(request, 'accounts/create_blog_post.html', {'form': form})
    else:
        return redirect('login')

def view_blog_posts(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            blog_posts = BlogPost.objects.filter(draft=False)
        else:
            blog_posts = BlogPost.objects.filter(author=request.user)
        return render(request, 'accounts/view_blog_posts.html', {'blog_posts': blog_posts})
    else:
        return redirect('login')
