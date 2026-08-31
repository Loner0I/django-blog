from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment


def post_list(request):
    posts = Post.objects.all()
    categories = Category.objects.all()

    category_slug = request.GET.get("category")
    if category_slug:
        posts = posts.filter(category__name=category_slug)

    return render(request, "blog/post_list.html", {
        "posts": posts,
        "categories": categories,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        if name and email and message:
            Comment.objects.create(post=post, name=name, email=email, message=message)
            return redirect("blog:post_detail", slug=post.slug)

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
    })
