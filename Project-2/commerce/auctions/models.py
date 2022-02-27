from django.contrib.auth.models import AbstractUser, User
from django.db import models




class User(AbstractUser):
    username = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254, unique = True)
    watchlist = models.ManyToManyField("Listing", related_name="watchlist")
    # bids = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="bids")

class Bid(models.Model):

    date_placed = models.DateField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=5, decimal_places=2)
    winning_bid = models.BooleanField(default=False)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
      

class Category(models.Model):
    title = models.CharField(max_length=64)

class Listing(models.Model):
    description = models.CharField(max_length=120)
    active = models.BooleanField(default=False)
    image = models.URLField(max_length=200, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    bids = models.ManyToManyField(Bid, related_name="bids")




