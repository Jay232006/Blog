from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count

@login_required
@require_POST
def like_blog(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if request.user in blog.liked_by.all():
        blog.liked_by.remove(request.user)
        liked = False
    else:
        blog.liked_by.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': blog.liked_by.count()
    })
def home(request):
    posts = BlogPost.objects.filter(visibility='public').order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_detail.html', {'blog': blog})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'status': 'success', 'message': 'User created successfully'})

    return render(request, 'Login.html')

def login_view(request):
    if request.method == "POST":
        username_or_email = request.POST.get('username_or_email')
        password = request.POST.get('password')
        user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"status": "success", "message": "Logged in successfully"})
        else:
            return JsonResponse({"status": "error", "message": "Invalid credentials"})

    return render(request, "Login.html")

@login_required(login_url='/login')
def create_blog_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        visibility = request.POST.get('visibility')
        image = request.FILES.get('image')
        tags = request.POST.get('tags')  # optional

        author = request.user

        BlogPost.objects.create(
            title=title,
            content=content,
            category=category,
            visibility=visibility,
            image=image,
            author=author
        )

        return redirect('home')

    return render(request, 'create.html')


from django.contrib.auth import logout

def profile_view(request):
    return render(request, 'profile.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def my_blogs(request):
    blogs = BlogPost.objects.filter(author=request.user)
    return render(request, 'my_blogs.html', {'blogs': blogs})

@login_required
def liked_blogs(request):
    # logic based on your model for liked blogs
    return render(request, 'liked.html')




def trending_view(request):
    trending_blogs = BlogPost.objects.annotate(num_likes=Count('liked_by')).order_by('-num_likes')
    return render(request, 'trending.html', {'trending_blogs': trending_blogs})


def explore_view(request):
    # You can customize this as needed
    return render(request, 'Explore.html')


from django.db.models import Count, Q

def explore_view(request):
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', '')

    blogs = BlogPost.objects.filter(visibility='public')

    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    if sort_option == 'newest':
        blogs = blogs.order_by('-created_at')
    elif sort_option == 'oldest':
        blogs = blogs.order_by('created_at')
    elif sort_option == 'likes':
        blogs = blogs.annotate(like_count=Count('liked_by')).order_by('-like_count')
    else:
        # Show top 5 blogs by likes by default
        blogs = blogs.annotate(like_count=Count('liked_by')).order_by('-like_count')[:5]

    return render(request, 'Explore.html', {'blogs': blogs})
