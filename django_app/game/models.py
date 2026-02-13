from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Play(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    story_id = models.IntegerField()
    ending_page_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class PlaySession(models.Model):
    session_id = models.CharField(max_length=255)
    story_id = models.IntegerField()
    current_page_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "story_id")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default="open")
    created_at = models.DateTimeField(auto_now_add=True)

class StoryOwnership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flask_story_id = models.IntegerField()
