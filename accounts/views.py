from django.shortcuts import render, redirect
from django.contrib.auth import login as sy_login
from django.contrib.auth import logout as sy_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from .forms import CustomForm, CustomChangeForm
from django.contrib.auth.decorators import login_required


def sign_up(request):
    if request.method == "POST":
        form = CustomForm(request.POST)
        if form.is_valid():
            sy_login(request, form.save())
            return redirect("articles:index")

    else:
        form = CustomForm()

    context = {"form": form}
    return render(request, "accounts/signup.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            sy_login(request, form.get_user())
            return redirect(request.GET.get("next") or "articles:index")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    articles = user.article_set.all()
    comments = user.comment_set.all()
    context = {
        "user": user,
        "articles": articles,
        "comments": comments,
    }
    return render(request, "accounts/detail.html", context)


def logout(request):
    sy_logout(request)
    return redirect("articles:index")


@login_required
def update(request):
    if request.method == "POST":
        form = CustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", request.user.pk)
    else:
        form = CustomChangeForm(instance=request.user)

    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:detail", request.user.pk)
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/change_password.html", context)


# Create your views here.
