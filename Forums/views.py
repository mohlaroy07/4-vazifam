from django.shortcuts import render, redirect, get_object_or_404
from .models import Topic, Comment, Profile
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

        data = {"user": request.user, "title": request.POST.get("title")}

        form = TopicForm(data)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.user = request.user
            topic.save()
            return redirect("homepage")
    else:
        form = TopicForm()
    return render(request, "home/create_topic.html", {"form": form})


def topic_detail(request, pk):
    topic = get_object_or_404(Topic, id=pk)
    comments = Comment.objects.filter(topic=topic)

    context = {"topic": topic, "comments": comments}

    if request.method == "POST":
        comment = request.POST.get("content")

        Comment.objects.create(topic=topic, description=comment, user=request.user)

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
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                return redirect("homepage")
            else:
                print("User", user)

    return render(request, "home/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("homepage")


def profile(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=user_id)
        topics = Topic.objects.filter(user=user)
        context = {"title": "User profile", "user": user, "topics": topics}
        try:
            user_profile = get_object_or_404(Profile, user=user)
            context["profile"] = user_profile
        except:
            pass
        return render(request, "home/profile.html", context)
    else:
        return redirect("login")
