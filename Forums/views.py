from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Comment
from .forms import TopicForm, CommentForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def homepage(request):
    topic_list = Topic.objects.all()
    context = {
        "topics": topic_list,
    }
    return render(request, "home/index.html", context=context)


def create_topic(request):
    if request.method == "POST":
        form = TopicForm(
            request.POST,
        )
        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect("create_topic", pk=topic.pk)
    else:
        form = TopicForm()
    return render(request, "home/create_topic.html", {"form": form})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, id=pk)

    context = {
        "topic": topic,
        "comment": topic.comment.all(),
    }
    if request.method == "POST":
        comment_list = request.POST.get("context")
        if comment_list:
            comment = topic.comments.create(
                context=comment_list, author=request.user, topic=topic
            )
            comment.save()
            return redirect("topic_detail", pk=pk)
    return render(request, "home/detail.html", context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")
    else:
        form = UserCreationForm()
    return render(request, "home/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
    if request.user.is_authenticated:
        user = request.user
        # user._meta ga murojaat qilish mumkin
    else:
        # Notanish foydalanuvchini boshqarish
        return redirect("user_login")

    return render(request, "home/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("homepage")
