from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="profiles")
    profile_id = models.IntegerField()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    no_likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "user": user.user,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
        
class Like(models.Model):
    post_id = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="liked_posts")
    fan = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liked_fans")

    def __str__(self):
        return self.fan

class Follower(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followees")

    def __str__(self):
        return self.user