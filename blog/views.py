from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import CommentForm


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
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=post,
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
            )
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = CommentForm()

    return render(request, "blog/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })
