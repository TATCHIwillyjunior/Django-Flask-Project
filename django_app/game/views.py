from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Play
import requests

FLASK_API_URL = 'http://127.0.0.1:5000'

def story_list(request):
    response = requests.get(f'{FLASK_API_URL}/stories')
    stories = response.json()
    return render(request, 'game/story_list.html', {'stories': stories})

def play_story(request, story_id):
    response = requests.get(f'{FLASK_API_URL}/stories/{story_id}/start')
    page = response.json()
    return render(request, 'game/play.html', {'page': page})

def make_choice(request, page_id, choice_id):
    response = requests.get(f'{FLASK_API_URL}/pages/{page_id}')
    page = response.json()
    choice = next(c for c in page['choices'] if c['id'] == int(choice_id))
    if page['is_ending']:
        Play.objects.create(story_id=page_id, ending_page_id=page_id)
    return redirect('play_story', story_id=page['id'])

def stats(request):
    plays = Play.objects.all()
    return render(request, 'game/stats.html', {'plays': plays})
