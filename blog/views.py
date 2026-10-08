from django.shortcuts import get_object_or_404, redirect, render
from blog.forms import CommentForm
from blog.models import Post, Comment

# Create your views here.
def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    context = {
        "posts": posts,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
    }
    return render(request, "blog/category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post).order_by("-created_on")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            return redirect("blog_detail", pk=post.pk)
    else:
        form = CommentForm()

    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/detail.html", context)


def delete_comment(request, comment_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("blog_index")

    comment = get_object_or_404(Comment, pk=comment_id)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("blog_detail", pk=post_pk)
