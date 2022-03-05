from django.contrib.auth.models import AbstractUser, User
from django.db import models




class User(AbstractUser):
    watchlists = models.ManyToManyField("Listing", blank=True, related_name="watchlists")

    # def __str__(self):
    #     return f'{self.first_name} {self.last_name}'

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
    current_bid = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")

    def __str__(self):
        return self.title

class Bid(models.Model):
    date_placed = models.DateField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=5, decimal_places=2)
    winning_bid = models.BooleanField(default=False)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    listings = models.ManyToManyField(Listing, blank=True, related_name="bids")

    # def __str__(self):
    #     return f'{self.id}: {self.bid_amount} by {user.username} for {listing.title}'    
    




