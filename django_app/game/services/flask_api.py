import requests
from django.conf import settings

BASE = settings.FLASK_API_BASE_URL
API_KEY = settings.FLASK_API_KEY

def get_published_stories():
    r = requests.get(f"{BASE}/stories", params={"status": "published"})
    r.raise_for_status()
    return r.json()

def get_story(story_id):
    r = requests.get(f"{BASE}/stories/{story_id}")
    r.raise_for_status()
    return r.json()

def get_story_start(story_id):
    r = requests.get(f"{BASE}/stories/{story_id}/start")
    r.raise_for_status()
    return r.json()

def get_page(page_id):
    r = requests.get(f"{BASE}/pages/{page_id}")
    r.raise_for_status()
    return r.json()

def create_story(data):
    r = requests.post(
        f"{BASE}/stories",
        json=data,
        headers={"X-API-KEY": API_KEY},
    )
    r.raise_for_status()
    return r.json()

# same pattern for update/delete, pages, choices
