from django.contrib.auth.models import AbstractUser, User
from django.db import models




class User(AbstractUser):
    username = models.CharField(max_length=50, unique = True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 254, unique = True)
    # watchlist = models.ManyToManyField("Listing", related_name="watchlist")

    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'

class Bid(models.Model):
    date_placed = models.DateField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=5, decimal_places=2)
    winning_bid = models.BooleanField(default=False)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")

    # def __str__(self):
    #     return f'{self.id}: {self.bid_amount} by {user.username} for {listing.title}'    
    

class Category(models.Model):
    title = models.CharField(max_length=64, default="None")

    def __str__(self):
        return self.title

class Listing(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    starting_bid = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    # bids = models.ManyToManyField(Bid, related_name="bids")

    def __str__(self):
        return self.title


