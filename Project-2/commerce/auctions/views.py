from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse

from .models import Category, User, Listing, Bid

# Add new listing form class
class NewListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'starting_bid', 'user', 'category']

# login view provided
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print(user)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

# logout view provided
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

# register view provided
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

#Home page view
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })
    
#Create view
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        
        if form.is_valid():
            form.save()
            message = "Success! New listing saved. Add another?"
            return render(request, "auctions/create.html", {
                "form": NewListingForm(),
                "message": message
            })
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })

#Individual Listing Page View
def listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    bids = listing.listing_bids.all()
    watchlists = listing.watchlists.all()
    # user = request.user
    # print(user)
    # non_watchlists = Users.objects.exclude(listings=listing).all()
    winning_bid_message = "Congratulations! Yours was the winning bid."
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "watchlists": watchlists,
        # "non_watchlists": non_watchlists,
        "winning_bid_message": winning_bid_message
    })

#Bid Form on Listing Page
def bidForm(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        bids = listing.listing_bids.all()
        user_bid = user
        listing_bid = listing
        bid_amount = int(request.POST["bid_amount"])
        current_bid = listing.current_bid
        if bid_amount > current_bid:
          current_bid = bid_amount
          listing.save()
          return HTTPResponseRedirect(reverse("listing", kwargs=('listing_id':listing.id)))
        # return render(request, "auctions/listing.html", {
        #     "listing": listing
        # })

#Comments Form on Listing Page
def commentForm(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user
        comments = listing.listing_comments.all()
        user_comment = user
        listing_comment = listing
        comment_post = request.POST["comment_post"]
        listing.listing_comments.add()

        # user_id = int(request.POST["user"])
        # user = User.objects.get(pk="user_id")
        return HTTPResponseRedirect(reverse("listing", args=(listing.id,)))

#Close Listing View
def close_listing(request, listing_id):
    if request.method=="POST":
        listing = Listing.objects.get(pk=listing_id)
        bids = listing.listing_bids.all()
        listing.active = False
        # if listing.current_bid >= listing.starting_bid:
        bid = Bid.objects.filter(bid_amount = listing.current_bid)
        bid.winning_bid = True
        # bid.listing_bid.save()
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing
        })
        # return HTTPResponseRedirect(reverse("listing", args=(listing.id,)))


#Watchlist Page View   
def watchlist(request, user_id):
    user = User.objects.get(id = user_id)
    watchlists = user.watchlists.all()
    listings = Listing.objects.all()
    print(user)
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "watchlists": watchlists,
        "listings": listings
    })

#Add Watchlist 
def watchlist_add(request, listing_id):
    if request.method=="POST":
        listing = listing.objects.get(pk=listing_id)
        user = request.user 
        user.watchlists.add()
        return HTTPResponseRedirect(reverse("listing", args=(listing.id,)))

#Remove Watchlist 
def watchlist_remove(request, listing_id):
    if request.method=="POST":
        listing = listing.objects.get(pk=listing_id)
        user = request.user
        user.watchlists.delete()
        return HTTPResponseRedirect(reverse("listing", args=(listing.id,)))

#Categories Page View 
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

# Individual Category Page View
def category(request, category_id):
    category = Category.objects.get(id = category_id)
    listings = Listing.objects.filter(category = category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })



