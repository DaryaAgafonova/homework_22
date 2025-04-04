from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.urls import reverse
from .models import BlogPost
from .forms import BlogPostForm

def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/blog_list.html', {'page_obj': page_obj})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk, is_published=True)
    post.increment_views()
    
    return render(request, 'blog/blog_detail.html', {'post': post})

@login_required
@permission_required('blog.add_blogpost', raise_exception=True)
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/blog_form.html', {'form': form, 'is_create': True})

@login_required
@permission_required('blog.change_blogpost', raise_exception=True)
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/blog_form.html', {'form': form, 'post': post, 'is_create': False})

@login_required
@permission_required('blog.delete_blogpost', raise_exception=True)
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    
    return render(request, 'blog/blog_delete.html', {'post': post})