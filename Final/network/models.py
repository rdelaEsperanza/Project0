from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("User", blank=True, default=[0], related_name="followers")

class Profile(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="profiles")
    profile_id = models.IntegerField()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(upload_to='images', default='images/default.jpg')
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

class Email(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
    recipients = models.ManyToManyField("User", related_name="emails_received")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.email,
            "recipients": [user.email for user in self.recipients.all()],
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "read": self.read,
            "archived": self.archived
        }