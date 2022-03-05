from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("create/", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bidForm", views.bidForm, name="bidForm"),
    path("<int:listing_id>/commentForm", views.commentForm, name="commentForm"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist")
]
