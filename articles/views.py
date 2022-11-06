from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .form import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib import messages
import os

# Create your views here.


def index(request):
    articles = Article.objects.all()
    context = {
        "articles": articles,
    }

    return render(request, "articles/index.html", context)


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    commentform = CommentForm()
    comments = article.comment_set.all()
    context = {
        "article": article,
        "commentform": commentform,
        "comments": comments,
    }
    return render(request, "articles/detail.html", context)


@login_required
def create(request):
    if request.method == "POST":
        article_form = ArticleForm(request.POST, request.FILES)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, "등록되었습니다.")
            return redirect("articles:index")
    else:
        article_form = ArticleForm()

        context = {
            "form": article_form,
        }

    return render(request, "articles/create.html", context)


@login_required
def update(request, pk):
    article = Article.objects.get(id=pk)
    if request.user == article.user:
        if request.method == "POST":
            article_form = ArticleForm(
                request.POST, request.FILES, instance=Article.objects.get(pk=pk)
            )
            if article_form.is_valid():
                if (
                    article.image and request.FILES.get("image") != None
                ) or request.POST.get("image-clear"):
                    os.remove(article.image.path)
                if (
                    article.thumbnail and request.FILES.get("thumbnail") != None
                ) or request.POST.get("thumbnail-clear"):
                    os.remove(article.thumbnail.path)
                article_form.save()
                messages.success(request, "수정되었습니다.")
                return redirect("articles:detail", article.pk)
        else:
            article_form = ArticleForm(instance=Article.objects.get(pk=pk))

            context = {
                "form": article_form,
            }
        return render(request, "articles/update.html", context)
    else:
        return redirect("articles:index")


#  article = Article.objects.get(pk=pk)
#     form = ArticleForm(
#         request.POST or None, request.FILES or None, instance=Article.objects.get(pk=pk)
#     )
#     if form.is_valid():
#         print(request.FILES)
#         if (article.image and request.FILES.get("image") != None) or request.POST.get(
#             "image-clear"
#         ):
#             os.remove(article.image.path)
#         if (
#             article.thumbnail and request.FILES.get("thumbnail") != None
#         ) or request.POST.get("thumbnail-clear"):
#             os.remove(article.thumbnail.path)
#         form.save()
#         return redirect("articles:detail", pk)
#     context = {
#         "form": form,
#     }
#     return render(request, "articles/create.html", context)


@login_required
def delete(request, pk):
    article = Article.objects.get(id=pk)
    if request.user == article.user:
        if request.method == "POST":
            if article.image:
                os.remove(article.image.path)
            if article.thumbnail:
                os.remove(article.thumbnail.path)
            article.delete()
            return redirect("articles:index")
    else:
        return redirect("article:index")


@login_required
def comment_creat(request, pk):
    article = Article.objects.get(pk=pk)
    commentform = CommentForm(request.POST)
    if commentform.is_valid():
        comment = commentform.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect("articles:detail", article.pk)


@login_required
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return redirect("articles:detail", article_pk)
    else:
        return redirect("articles:detail", article_pk)


@login_required
def comment_update(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    article = Article.objects.get(pk=article_pk)
    if request.user == comment.user:
        if request.method == "POST":
            commentform = CommentForm(request.POST, instance=comment)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.article = article
                comment.save()
                return redirect("articles:detail", article.pk)

        else:
            commentform = CommentForm(instance=comment)

        context = {
            "commentform": commentform,
        }
        return render(request, "articles/comment_update.html", context)
    else:
        return redirect("articles:detail", article.pk)
