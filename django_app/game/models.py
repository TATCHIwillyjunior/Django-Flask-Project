from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Play(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story_id = models.IntegerField()
    ending_page_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Play {self.id}: User {self.user.username}, Story {self.story_id}, Ending {self.ending_page_id}"


class PlaySession(models.Model):
    session_key = models.CharField(max_length=255, db_index=True)
    story_id = models.IntegerField()
    current_page_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session_key', 'story_id')

    def __str__(self):
        return f"Session {self.session_key} on story {self.story_id} at page {self.current_page_id}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('author', 'Author'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
