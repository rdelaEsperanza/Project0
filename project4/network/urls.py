
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like, name="like"),
    path("comment", views.comment, name="comment"),
    path("edit_comment", views.edit_comment, name="edit_comment")
]
