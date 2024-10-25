from django.urls import path
from .views import (
    homepage,
    create_topic,
    topic_detail,
    register,
    user_login,
    log_out,
    profile,
)

urlpatterns = [
    path("", homepage, name="homepage"),
    path("create/", create_topic, name="create_topic"),
    path("topic_detail/<int:pk>/", topic_detail, name="topic_detail"),
    path("login/", user_login, name="user_login"),
    path("register/", register, name="register"),
    path("logout/", log_out, name="logout"),
    path("profile/<int:user_id>/", profile, name="profile"),
]
