from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User, Profile, Post, Like, Follower


@login_required(login_url='login')
def index(request):

    posts = Post.objects.all()
    return render(request, "network/index.html", {'posts':posts})




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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required(login_url='login')
def comment(request):
    if request.method == "POST":
        user = request.user
        body = request.POST["body"]

        new_post = Post.objects.create(user=user, body=body)
        new_post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return redirect('/')

@login_required(login_url='login')
def edit_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post.id")
        print(post_id)
        post = Post.objects.get(id = post_id)
        post.body = request.POST["body"]
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return redirect('/')

@login_required(login_url='login')
def profile(request, user_id):
    target_user = User.objects.get(id = user_id)
    user_profile = Profile.objects.get(user = target_user)
    user_posts = Post.objects.filter(user = target_user)
    user_no_posts = len(user_posts)

    follower = request.user
    followee = target_user

    if Follower.objects.filter(follower = follower, user = followee).first():
        cta_text = "Unfollow"
    else:
        cta_text = "Follow"

    profile_followers = len(Follower.objects.filter(user=user_id))
    profiles_following = len(Follower.objects.filter(follower=user_id))

    return render(request, "network/profile.html", {
        "followee": followee,
        "follower": follower,
        "user_profile": user_profile,
        "user_posts": user_posts,
        "user_no_posts": user_no_posts,
        "cta_text": cta_text,
        "profile_followers": profile_followers,
        "profiles_following": profiles_following
    })

@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]
        followee = request.POST["followee"]

        if Follower.objects.filter(follower = follower, user = followee).first():
            delete_follower = Follower.objects.get(follower = follower, user = followee)
            delete_follower.delete()
            return HttpResponseRedirect(reverse("profile/"+followee))
        else:
            new_follower = Follower.objects.create(follower = follower, user = followee)
            new_follower.save()
            return HttpResponseRedirect(reverse("profile/"+followee))

    else:
     return HttpResponseRedirect(reverse("index"))

@login_required(login_url='login')
def following(request):
    pass
    return render(request, "network/following.html")

@login_required(login_url='login')
def like(request, post_id):
    user = request.user
    # post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)

    like_check = Like.objects.filter(post_id = post.id, fan = user).first()

    if like_check == None:
        new_like = Like.objects.create(post_id = post, fan = user)
        new_like.save()
        post.no_likes = post.no_likes+1
        post.save()
        return HttpResponseRedirect(reverse("index"))
        
    else:
        like_check.delete()
        post.no_likes = post.no_likes-1
        post.save()
        return HttpResponseRedirect(reverse("index"))

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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
