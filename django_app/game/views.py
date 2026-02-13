from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import Play, PlaySession
from .services import flask_api

# Create your views here.

def story_list(request):
    stories = flask_api.get_published_stories()
    return render(request, "game/story_list.html", {"stories": stories})

def _get_session_id(request):
    sid = request.COOKIES.get("play_session_id")
    if not sid:
        sid = get_random_string(32)
    return sid

def play_start(request, story_id):
    start_page = flask_api.get_story_start(story_id)
    response = redirect("play_page", page_id=start_page["id"])
    # ensure session cookie exists
    sid = _get_session_id(request)
    response.set_cookie("play_session_id", sid)
    return response

def play_page(request, page_id):
    page = flask_api.get_page(page_id)
    story_id = page["story_id"]

    # auto-save progression (anonymous)
    sid = _get_session_id(request)
    PlaySession.objects.update_or_create(
        session_id=sid,
        story_id=story_id,
        defaults={"current_page_id": page_id},
    )

    if request.method == "POST":
        next_page_id = int(request.POST["next_page_id"])
        return redirect("play_page", page_id=next_page_id)

    # ending reached
    if page["is_ending"]:
        ending_page_id = page["id"]
        Play.objects.create(
            user=request.user if request.user.is_authenticated else None,
            story_id=story_id,
            ending_page_id=ending_page_id,
        )
        return render(request, "game/ending.html", {"page": page})

    return render(request, "game/page.html", {"page": page})
