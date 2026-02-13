from .models import StoryOwnership

def user_owns_story(user, story_id):
    return StoryOwnership.objects.filter(
        user=user,
        flask_story_id=story_id
    ).exists()
