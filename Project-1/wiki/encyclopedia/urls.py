from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit"),
    path("error/", views.error, name="errors"),
    path("random/", views.random_page, name="random"),
    path("wiki/", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry")
]
