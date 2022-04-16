from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
# from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import User, Profile, Post, Like

# class PostListView(ListView):
#     paginate_by = 10
#     model = Post

@login_required(login_url='login')
def index(request):

    posts = Post.objects.all()
    # post_list = Post.objects.all()
    # paginator = Paginator(post_list, 10)

    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {'posts':posts})
    # return render(request, "network/index.html", {"page_obj" : page_obj})




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
        post_id = request.POST.get("post-id")
        print(post_id)
        post = Post.objects.get(id = post_id)
        post.body = request.POST["body"]
        post.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return redirect('/')

@login_required(login_url='login')
def profile(request, user_id):
    profile_user = User.objects.get(id = user_id)
    if Profile.objects.filter(user = profile_user).exists():
        user_profile = Profile.objects.get(user = profile_user)
        user_posts = Post.objects.filter(user = profile_user)
        user_no_posts = len(user_posts)
        no_followers = profile_user.followers.count()
        no_following = User.objects.filter(following = profile_user).count()
        
        print(no_followers, no_following)
    else:
        user_profile = "none"
        user_posts = "none"
        user_no_posts = "none"
        no_followers = "none"
        no_following = "none"
        
    follower = request.user
    followee = profile_user

    if profile_user in follower.following.all():
        cta_text = "Unfollow"
    else:
        cta_text = "Follow"

    return render(request, "network/profile.html", {
        "followee": followee,
        "follower": follower,
        "user_profile": user_profile,
        "user_posts": user_posts,
        "user_no_posts": user_no_posts,
        "cta_text": cta_text,
        "no_followers": no_followers,
        "no_following": no_following
    })

@login_required(login_url='login')
def follow(request):
    if request.method == "POST":
        follower_id = request.POST["follower"]
        followee_id = request.POST["followee"]
        print(follower_id, " ", followee_id)
        follower = User.objects.get(id = follower_id)
        followee = User.objects.get(id = followee_id)
        
        if follower in followee.followers.all():
            followee.followers.remove(request.user)
            return HttpResponseRedirect(reverse("profile", args=(followee_id,)))
        else:
            followee.followers.add(request.user)
            print(followee.followers)
            return HttpResponseRedirect(reverse("profile", args=(followee_id,)))

    else:
     return redirect('/')

@login_required(login_url='login')
def following(request):
    user = User.objects.get(id = request.user.id)
    user_following = User.objects.filter(followers = user)
    # user_following = User.objects.filter(id = user.following.all())
    posts = Post.objects.all(user = user_following)
    print(posts)
    return render(request, "network/following.html", {
        "user": user,
        "user_following": user_following,
        "posts": posts
    })

@login_required(login_url='login')
def like(request, post_id):
    user = request.user
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
