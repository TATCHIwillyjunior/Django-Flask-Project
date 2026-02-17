from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Play, PlaySession
import requests
from django.utils import timezone

FLASK_API_URL = 'http://127.0.0.1:5000'

def story_list(request):
    query = request.GET.get('q', '').strip()

    params = {'status': 'published'}
    if query:
        params['q'] = query

    response = requests.get(f'{FLASK_API_URL}/stories', params=params)
    stories = response.json()

    return render(request, 'game/story_list.html', {
        'stories': stories,
        'query': query,
    })


# def story_list(request): query = request.GET.get("q", "").strip() # Fetch only published stories from Flask resp = requests.get(f"{FLASK_BASE_URL}/stories", params={"status": "published"}) stories = resp.json() # Apply search filter locally if query: stories = [ s for s in stories if query.lower() in s["title"].lower() ] return render(request, "game/story_list.html", { "stories": stories, "query": query, })

# django_app/game/views.py
def play_story(request, story_id):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    try:
        session = PlaySession.objects.get(session_key=session_key, story_id=story_id)
        return redirect('play_page', story_id=story_id, page_id=session.current_page_id)
    except PlaySession.DoesNotExist:
        pass

    response = requests.get(f'{FLASK_API_URL}/stories/{story_id}/start')
    if response.status_code != 200:
        messages.error(request, "Error loading story: " + response.json().get('error', 'Unknown error'))
        return redirect('story_list')

    page = response.json()

    PlaySession.objects.create(
    session_key=session_key,
    story_id=story_id,
    current_page_id=page['id']
)


    return render(request, 'game/play.html', {'page': page, 'story_id': story_id})


def play_page(request, story_id, page_id):
    session_key = request.session.session_key
    if session_key:
        PlaySession.objects.filter(session_key=session_key, story_id=story_id).update(
            current_page_id=page_id,
            updated_at=timezone.now()
        )

    response = requests.get(f'{FLASK_API_URL}/pages/{page_id}')
    if response.status_code != 200:
        messages.error(request, "Error loading page: " + response.json().get('error', 'Unknown error'))
        return redirect('story_list')

    page = response.json()
    return render(request, 'game/play.html', {'page': page, 'story_id': story_id})

def make_choice(request, story_id, page_id, choice_id):
    response = requests.get(f'{FLASK_API_URL}/pages/{page_id}')
    if response.status_code != 200:
        messages.error(request, "Error loading page: " + response.json().get('error', 'Unknown error'))
        return redirect('play_page', story_id=story_id, page_id=page_id)

    page = response.json()
    choice = next((c for c in page['choices'] if c['id'] == choice_id), None)
    if not choice:
        messages.error(request, "Invalid choice selected")
        return redirect('play_page', story_id=story_id, page_id=page_id)

    next_page_response = requests.get(f'{FLASK_API_URL}/pages/{choice["next_page_id"]}')
    if next_page_response.status_code != 200:
        messages.error(request, "Error loading next page: " + next_page_response.json().get('error', 'Unknown error'))
        return redirect('play_page', story_id=story_id, page_id=page_id)

    next_page = next_page_response.json()

    if next_page['is_ending']:
        Play.objects.create(story_id=story_id, ending_page_id=next_page['id'])

    return redirect('play_page', story_id=story_id, page_id=choice['next_page_id'])

def stats(request, story_id=None):
    if story_id:
        plays = Play.objects.filter(story_id=story_id)
        total_plays = plays.count()
        endings = {}
        for play in plays:
            ending_id = play.ending_page_id
            endings[ending_id] = endings.get(ending_id, 0) + 1

        ending_labels = {}
        for ending_id in endings.keys():
            response = requests.get(f'{FLASK_API_URL}/pages/{ending_id}')
            if response.status_code == 200:
                ending_page = response.json()
                ending_labels[ending_id] = ending_page.get('ending_label', f'Ending {ending_id}')
            else:
                ending_labels[ending_id] = f'Ending {ending_id}'

        ending_percentages = {ending_id: (count / total_plays) * 100 for ending_id, count in endings.items()}

        response = requests.get(f'{FLASK_API_URL}/stories/{story_id}')
        story = response.json() if response.status_code == 200 else {'id': story_id, 'title': 'Unknown Story'}

        return render(request, 'game/story_stats.html', {
            'story': story,
            'total_plays': total_plays,
            'ending_percentages': ending_percentages,
            'ending_labels': ending_labels
        })
    else:
        plays = Play.objects.all()
        plays_per_story = {}
        for play in plays:
            plays_per_story[play.story_id] = plays_per_story.get(play.story_id, 0) + 1

        stories_response = requests.get(f'{FLASK_API_URL}/stories')
        stories = {}
        if stories_response.status_code == 200:
            stories = {story['id']: story['title'] for story in stories_response.json()}

        return render(request, 'game/stats.html', {
            'plays_per_story': plays_per_story,
            'stories': stories
        })

def preview_story(request, story_id):
    response = requests.get(f'{FLASK_API_URL}/stories/{story_id}/start')
    if response.status_code != 200:
        messages.error(request, "Error loading story: " + response.json().get('error', 'Unknown error'))
        return redirect('story_list')

    page = response.json()
    return render(request, 'game/preview.html', {'page': page, 'story_id': story_id})

def preview_page(request, story_id, page_id):
    response = requests.get(f'{FLASK_API_URL}/pages/{page_id}')
    if response.status_code != 200:
        messages.error(request, "Error loading page: " + response.json().get('error', 'Unknown error'))
        return redirect('story_list')

    page = response.json()
    return render(request, 'game/preview.html', {'page': page, 'story_id': story_id})

def delete_story(request, story_id):
    if request.method == 'POST':
        try:
            response = requests.delete(f'{FLASK_API_URL}/stories/{story_id}')
            if response.status_code == 200:
                messages.success(request, 'Story deleted successfully!')
                return redirect('story_list')
            else:
                messages.error(request, f'Error deleting story: {response.json().get("error", "Unknown error")}')
        except Exception as e:
            messages.error(request, f'Error connecting to API: {str(e)}')

    return redirect('story_list')
