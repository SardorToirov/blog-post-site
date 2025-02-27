from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm

@login_required(login_url='home:login')
def logout_page(request):
    if request.method == "POST":  # Faqat POST so‘rovga ruxsat beriladi
        logout(request)
        return redirect(request.META.get('HTTP_REFERER', 'home:home'))
    return redirect('home:home')  # Agar noto‘g‘ri so‘rov bo‘lsa, bosh sahifaga qaytaradi

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home:home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home:login')

    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('home:register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('home:login')

    return render(request, 'register.html')

class PostList(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(status="published")

@login_required(login_url='home:login')
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post, slug=slug, status='published',
        publish__year=year, publish__month=month, publish__day=day
    )
    post_url = request.build_absolute_uri(post.get_absolute_url())
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        if 'like' in request.POST:
            post.likes += 1
            post.save()
            messages.success(request, "You liked the post!")
            return redirect(post.get_absolute_url())

        else:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
                messages.success(request, "Comment added successfully!")
                return redirect(post.get_absolute_url())

    else:
        comment_form = CommentForm()

    return render(request, 'detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'post_url': post_url,
    })
