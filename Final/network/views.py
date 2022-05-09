import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import User, Profile, Post, Like, Email 


@login_required(login_url='login')
def index(request):

    # posts = Post.objects.all()
    post_list = Post.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    return render(request, "network/index.html", {'posts':posts})

def inbox(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "network/inbox.html")

    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


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
        image = request.FILES.get('post_image')
        new_post = Post.objects.create(user=user, body=body, image=image)
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

@csrf_exempt
@login_required
def compose(request):

    # Composing a new message must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Check recipient emails
    data = json.loads(request.body)
    emails = [email.strip() for email in data.get("recipients").split(",")]
    if emails == [""]:
        return JsonResponse({
            "error": "At least one recipient required."
        }, status=400)

    # Convert email addresses to users
    recipients = []
    for email in emails:
        try:
            user = User.objects.get(email=email)
            recipients.append(user)
        except User.DoesNotExist:
            return JsonResponse({
                "error": f"User with email {email} does not exist."
            }, status=400)

    # Get contents of email
    body = data.get("body", "")

    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    users.update(recipients)
    for user in users:
        email = Email(
            user=user,
            sender=request.user,
            body=body,
            read=user == request.user
        )
        email.save()
        for recipient in recipients:
            email.recipients.add(recipient)
        email.save()

    return JsonResponse({"message": "email sent successfully."}, status=201)

@login_required
def mailbox(request, mailbox):

    # Filter emails returned based on mailbox
    # if mailbox == "inbox":
    #     emails = Email.objects.filter(
    #         user=request.user, recipients=request.user, archived=False
    #     )
    # elif mailbox == "sent":
    #     emails = Email.objects.filter(
    #         user=request.user, sender=request.user
    #     )
    # elif mailbox == "archive":
    #     emails = Email.objects.filter(
    #         user=request.user, recipients=request.user, archived=True
    #     )

    # Filter messages based on user
    
    if mailbox == "all":
        emails = Email.objects.filter(
            (Q(sender=request.user) | Q(recipients=request.user))
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    emails = emails.order_by("-timestamp").all()
    return JsonResponse([email.serialize() for email in emails], safe=False)

@csrf_exempt
@login_required
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    # email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)



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
    posts = Post.objects.filter(user__in = user.following.all())
    return render(request, "network/following.html", {
        "user": user,
        # "user_following": user_following,
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
