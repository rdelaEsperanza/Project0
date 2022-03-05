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
            # title = form.cleaned_data["title"]
            # description = form.cleaned_data["description"]
            # image_url = form.cleaned_data["image_url"]
            # starting_bid = forms.DecimalField(hep_text="What is the minimum acceptable bid?")
            # user = forms.CharField()
            # category = forms.Charfield(label="Category")
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
    winning_bid_message = "Congratulations! Yours was the winning bid."
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "winning_bid_message": winning_bid_message
    })

#Watchlist Page View   
def watchlist(request):
    user = request.user.username
    return render(request, "auctions/watchlist.html", {
        "Listings": Listing.objects.all(),
        "user": user
    })

#Categories Page View 
def categories(request):
    return render(request, "auctions/categories.html", {
        "Categories": Category.objects.all()
    })

#Individual Category Page View
def category(request, category_id):
    category = Category.objects.get(id = category_id)
    return render(request, "auctions/category.html", {
        "category": category
    })

