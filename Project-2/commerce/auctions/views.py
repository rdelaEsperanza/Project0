from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse

from .models import Category, User, Listing, Bid


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def index(request):
    return render(request, "auctions/index.html")

def create(request):
    pass
    # if request.method == "POST":
    #     form = NewEntryForm(request.POST)
        
    #     if form.is_valid():
    #         title = form.cleaned_data["entry_title"]
    #         entry_markdown = form.cleaned_data["entry_markdown"]
    #         print(title)
    #         if title == util.get_entry(title):
    #             raise ValidationError(f"This title already exists")
    #         util.save_entry(title, entry_markdown)
    #         # return HttpResponseRedirect(reverse(entry, args=(title,)))
    #         converted_md = markdowner.convert(entry_markdown)
    #         return render(request, "encyclopedia/entry.html", {
    #             "title": title.capitalize(),
    #             "markdown": converted_md
    #         })
    #     else:
    #         return render(request, "encyclopedia/create.html", {
    #             "form": form
    #         })


    # return render(request, "encyclopedia/create.html", {
    #     "form": NewEntryForm()
    # })

def listing(request):
    pass

    
def watchlist(request):
    pass

def categories(request):
    pass

