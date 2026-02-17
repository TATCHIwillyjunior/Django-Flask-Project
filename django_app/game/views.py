from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Play, PlaySession
import requests
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from .forms import RegisterForm
from .models import Play, PlaySession, Profile


FLASK_API_URL = 'http://127.0.0.1:5000'

# Decorator to check if user is an author or admin
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            profile = user.profile
            profile.role = form.cleaned_data['role']
            profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'game/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('story_list')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'game/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

# Story Endpoints
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
    # Check story status first
    story_resp = requests.get(f"{FLASK_API_URL}/stories/{story_id}")
    if story_resp.status_code != 200:
        messages.error(request, "Error loading story.")
        return redirect('story_list')

    story_data = story_resp.json()
    if story_data.get("status") == "suspended":
        messages.error(request, "This story is suspended and cannot be played.")
        return redirect("story_list")

    # Session handling (auto-save)
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

# Handle choice selection and auto-saving playthroughs
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
        if request.user.is_authenticated:
            Play.objects.create(
                user=request.user,
                story_id=story_id,
                ending_page_id=next_page['id']
            )
        else:
            messages.info(request, "Ending reached (not saved because you are not logged in).")

    return redirect('play_page', story_id=story_id, page_id=choice['next_page_id'])


def stats(request, story_id=None):
    """
    Level 16-compliant statistics:
    - Readers: only see their own plays
    - Authors/Admins: see global stats
    """

    # Determine user role
    user = request.user
    role = None
    if user.is_authenticated:
        role = getattr(user.profile, "role", None)

    # -------------------------------
    # STORY-SPECIFIC STATS
    # -------------------------------
    if story_id:
        # Readers → only their own plays
        if user.is_authenticated and role == "reader" and not user.is_staff:
            plays = Play.objects.filter(story_id=story_id, user=user)
        else:
            plays = Play.objects.filter(story_id=story_id)

        total_plays = plays.count()

        # Count endings
        endings = {}
        for play in plays:
            ending_id = play.ending_page_id
            endings[ending_id] = endings.get(ending_id, 0) + 1

        # Fetch ending labels from Flask
        ending_labels = {}
        for ending_id in endings.keys():
            response = requests.get(f'{FLASK_API_URL}/pages/{ending_id}')
            if response.status_code == 200:
                ending_page = response.json()
                ending_labels[ending_id] = ending_page.get('ending_label', f'Ending {ending_id}')
            else:
                ending_labels[ending_id] = f'Ending {ending_id}'

        # Percentages
        ending_percentages = {}
        if total_plays > 0:
            ending_percentages = {
                ending_id: (count / total_plays) * 100
                for ending_id, count in endings.items()
            }

        # Fetch story info
        response = requests.get(f'{FLASK_API_URL}/stories/{story_id}')
        story = response.json() if response.status_code == 200 else {'id': story_id, 'title': 'Unknown Story'}

        return render(request, 'game/story_stats.html', {
            'story': story,
            'total_plays': total_plays,
            'ending_percentages': ending_percentages,
            'ending_labels': ending_labels
        })

    # -------------------------------
    # GLOBAL STATS (ALL STORIES)
    # -------------------------------
    else:
        # Readers → only their own plays
        if user.is_authenticated and role == "reader" and not user.is_staff:
            plays = Play.objects.filter(user=user)
        else:
            plays = Play.objects.all()

        # Count plays per story
        plays_per_story = {}
        for play in plays:
            plays_per_story[play.story_id] = plays_per_story.get(play.story_id, 0) + 1

        # Fetch story titles
        stories_response = requests.get(f'{FLASK_API_URL}/stories')
        stories = {}
        if stories_response.status_code == 200:
            stories = stories_response.json()  # list of story dicts


        return render(request, 'game/stats.html', {
            'plays_per_story': plays_per_story,
            'stories': stories
        })

# Author/Admin story management views
# Only authors of the story or admins can access these views (enforced by decorator)
@staff_member_required
def suspend_story(request, story_id):
    if request.method == 'POST':
        try:
            resp = requests.put(
                f"{FLASK_API_URL}/stories/{story_id}",
                json={"status": "suspended"},
                headers={"X-API-KEY": settings.FLASK_API_KEY}
            )
            if resp.status_code == 200:
                messages.success(request, "Story suspended.")
            else:
                messages.error(request, f"Error suspending story: {resp.json().get('error', 'Unknown error')}")
        except Exception as e:
            messages.error(request, f"Error connecting to API: {str(e)}")
        return redirect('story_list')

    return render(request, 'game/suspend_confirm.html', {'story_id': story_id})


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
