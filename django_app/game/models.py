# django_app/game/models.py
from django.db import models
from django.utils import timezone

class Play(models.Model):
    story_id = models.IntegerField()
    ending_page_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Play {self.id}: Story {self.story_id}, Ending {self.ending_page_id}"


class PlaySession(models.Model):
    session_key = models.CharField(max_length=255)
    story_id = models.IntegerField()
    current_page_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session_key', 'story_id')


    def __str__(self):
        return f"Session {self.session_key} on story {self.story_id} at page {self.current_page_id}"
