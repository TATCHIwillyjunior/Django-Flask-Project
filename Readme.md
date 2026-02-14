# Django–Flask Interactive Story Project

This project is a full‑stack web application combining **Flask (backend API)** and **Django (frontend interface)** to create and manage interactive branching stories.  
It was developed as part of the **Python for Web Development Final Project**.

---

## 🚀 Project Overview

The application allows users to:

- Create stories  
- Add pages to each story  
- Add choices that connect pages  
- Build branching narrative structures  
- Interact with the story through a clean UI (Django)  
- Manage data through a REST API (Flask)

The backend exposes a structured API for Stories, Pages, and Choices, while the frontend consumes this API to display and navigate interactive stories.

---

## 🧱 Project Architecture

Today
create 10 for each:
It looks like you want me to create 10 items for each category, but you didn’t specify what the categories are.
Do you want:

10 ideas for your Django/Flask project?

10 tasks for your final project roadmap?

10 improvements for your GitHub repo?

10 LinkedIn post ideas?

10 debugging steps for your JSONDecodeError?

Something else entirely?

Give me the categories you want, and I’ll generate 10 items for each—clean, structured, and tailored to your project and workflow.

# Models
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='draft')
    start_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(100))
    story = db.relationship('Story', backref='pages')

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page = db.relationship('Page', backref='choices')
Great — now that I see your SQLAlchemy models, I understand what you meant earlier.
You want 10 examples for each model so you can seed your database or test your story engine.

Below is a clean, structured set of 10 Stories, 10 Pages, and 10 Choices, all consistent with your schema and ready to adapt into fixtures or seed scripts.

10 Story Examples
Each story has: title, description, status, start_page_id.

Stories
The Lost Amulet — A young hero searches for a magical relic. — draft — start_page_id: 1

Escape from Solaris Station — A sci‑fi thriller about a failing space station. — published — start_page_id: 11

The Forest of Echoes — A mysterious forest that repeats your thoughts. — draft — start_page_id: 21

Chronicles of the Iron Kingdom — A medieval kingdom on the brink of war. — draft — start_page_id: 31

Cyber Runner — A hacker navigating a dystopian megacity. — published — start_page_id: 41

The Time Loop Café — A café where every day repeats. — draft — start_page_id: 51

Voyage of the Silver Whale — A fantasy adventure on a flying ship. — draft — start_page_id: 61

The Last Oracle — A world where prophecies are illegal. — published — start_page_id: 71

Underworld Delivery Service — A courier delivering packages to supernatural beings. — draft — start_page_id: 81

The Neon Tournament — A futuristic combat competition. — published — start_page_id: 91

10 Page Examples
Each page has: story_id, text, is_ending, ending_label.

Pages
Story 1 — “You wake up in a ruined temple, the amulet missing.” — not ending

Story 1 — “A shadowy figure appears holding the amulet.” — ending: true — “Bad Ending: Too Late”

Story 2 — “Alarms blare as Solaris Station loses power.” — not ending

Story 2 — “You reach the escape pod bay.” — ending: true — “Survivor Ending”

Story 3 — “Whispers echo your name as you enter the forest.” — not ending

Story 3 — “You become one with the forest.” — ending: true — “Spirit Ending”

Story 4 — “The king summons you to the war council.” — not ending

Story 4 — “The kingdom falls to invaders.” — ending: true — “Defeat Ending”

Story 5 — “Neon lights flicker as drones scan the streets.” — not ending

Story 5 — “You hack the central AI and free the city.” — ending: true — “Revolution Ending”

10 Choice Examples
Each choice has: page_id, text, next_page_id.

Choices
Page 1 — “Search the temple ruins” → Page 2

Page 1 — “Follow the footprints outside” → Page 3

Page 3 — “Run to the escape pods” → Page 4

Page 3 — “Try to restore power manually” → Page 5

Page 5 — “Enter deeper into the forest” → Page 6

Page 5 — “Retreat to the village” → Page 7

Page 7 — “Accept the king’s mission” → Page 8

Page 7 — “Refuse and flee the kingdom” → Page 9

Page 9 — “Hack the drone network” → Page 10

Page 9 — “Hide in the alleyway” → Page 11

If you want, I can also generate:

SQLAlchemy seed script

JSON fixtures

Automatic graph visualization of story branching

Admin UI mockups

API endpoints for CRUD operations

Just tell me what direction you want to take next.

in postman formate
Here you go — your models formatted exactly the way Postman expects for JSON body requests.
I’ll give you 10 examples for each model in clean, ready‑to‑paste Postman JSON arrays.

📌 10 Stories — Postman JSON Format
json
[
  {
    "title": "The Lost Amulet",
    "description": "A young hero searches for a magical relic.",
    "status": "draft",
    "start_page_id": 1
  },
  {
    "title": "Escape from Solaris Station",
    "description": "A sci-fi thriller about a failing space station.",
    "status": "published",
    "start_page_id": 11
  },
  {
    "title": "The Forest of Echoes",
    "description": "A mysterious forest that repeats your thoughts.",
    "status": "draft",
    "start_page_id": 21
  },
  {
    "title": "Chronicles of the Iron Kingdom",
    "description": "A medieval kingdom on the brink of war.",
    "status": "draft",
    "start_page_id": 31
  },
  {
    "title": "Cyber Runner",
    "description": "A hacker navigating a dystopian megacity.",
    "status": "published",
    "start_page_id": 41
  },
  {
    "title": "The Time Loop Café",
    "description": "A café where every day repeats.",
    "status": "draft",
    "start_page_id": 51
  },
  {
    "title": "Voyage of the Silver Whale",
    "description": "A fantasy adventure on a flying ship.",
    "status": "draft",
    "start_page_id": 61
  },
  {
    "title": "The Last Oracle",
    "description": "A world where prophecies are illegal.",
    "status": "published",
    "start_page_id": 71
  },
  {
    "title": "Underworld Delivery Service",
    "description": "A courier delivering packages to supernatural beings.",
    "status": "draft",
    "start_page_id": 81
  },
  {
    "title": "The Neon Tournament",
    "description": "A futuristic combat competition.",
    "status": "published",
    "start_page_id": 91
  }
]
📌 10 Pages — Postman JSON Format
json
[
  {
    "story_id": 1,
    "text": "You wake up in a ruined temple, the amulet missing.",
    "is_ending": false,
    "ending_label": null
  },
  {
    "story_id": 1,
    "text": "A shadowy figure appears holding the amulet.",
    "is_ending": true,
    "ending_label": "Bad Ending: Too Late"
  },
  {
    "story_id": 2,
    "text": "Alarms blare as Solaris Station loses power.",
    "is_ending": false,
    "ending_label": null
  },
  {
    "story_id": 2,
    "text": "You reach the escape pod bay.",
    "is_ending": true,
    "ending_label": "Survivor Ending"
  },
  {
    "story_id": 3,
    "text": "Whispers echo your name as you enter the forest.",
    "is_ending": false,
    "ending_label": null
  },
  {
    "story_id": 3,
    "text": "You become one with the forest.",
    "is_ending": true,
    "ending_label": "Spirit Ending"
  },
  {
    "story_id": 4,
    "text": "The king summons you to the war council.",
    "is_ending": false,
    "ending_label": null
  },
  {
    "story_id": 4,
    "text": "The kingdom falls to invaders.",
    "is_ending": true,
    "ending_label": "Defeat Ending"
  },
  {
    "story_id": 5,
    "text": "Neon lights flicker as drones scan the streets.",
    "is_ending": false,
    "ending_label": null
  },
  {
    "story_id": 5,
    "text": "You hack the central AI and free the city.",
    "is_ending": true,
    "ending_label": "Revolution Ending"
  }
]
📌 10 Choices — Postman JSON Format
json
[
  {
    "page_id": 1,
    "text": "Search the temple ruins",
    "next_page_id": 2
  },
  {
    "page_id": 1,
    "text": "Follow the footprints outside",
    "next_page_id": 3
  },
  {
    "page_id": 3,
    "text": "Run to the escape pods",
    "next_page_id": 4
  },
  {
    "page_id": 3,
    "text": "Try to restore power manually",
    "next_page_id": 5
  },
  {
    "page_id": 5,
    "text": "Enter deeper into the forest",
    "next_page_id": 6
  },
  {
    "page_id": 5,
    "text": "Retreat to the village",
    "next_page_id": 7
  },
  {
    "page_id": 7,
    "text": "Accept the king’s mission",
    "next_page_id": 8
  },
  {
    "page_id": 7,
    "text": "Refuse and flee the kingdom",
    "next_page_id": 9
  },
  {
    "page_id": 9,
    "text": "Hack the drone network",
    "next_page_id": 10
  },
  {
    "page_id": 9,
    "text": "Hide in the alleyway",
    "next_page_id": 11
  }
]
Want me to generate a full Postman collection (.json) with:
folders (Stories, Pages, Choices)

POST, GET, PUT, DELETE requests

example bodies pre‑filled with these items

environment variables (e.g., {{base_url}})

I can prepare it cleanly so you can import it directly into Postman.

yeah and in order I don't want to dealswith error
Got you — you want everything in order, clean, consistent, and ready to paste into Postman without causing JSONDecodeError.
And don’t worry about the Edge tabs — your request is not related to any of them, so I won’t use them here.

Let’s build this properly.

✅ FULLY ORDERED POSTMAN‑READY DATASET
Everything is structured so that:

Stories come first

Pages reference valid story IDs

Choices reference valid page IDs

No circular references

No missing IDs

No invalid foreign keys

No nulls where not allowed

This is the safest way to avoid JSONDecodeError when seeding your API.

📌 1. STORIES (IDs 1–10)
Paste this into Postman → Body → raw → JSON

json
[
  {
    "id": 1,
    "title": "The Lost Amulet",
    "description": "A young hero searches for a magical relic.",
    "status": "draft",
    "start_page_id": 1
  },
  {
    "id": 2,
    "title": "Escape from Solaris Station",
    "description": "A sci-fi thriller about a failing space station.",
    "status": "published",
    "start_page_id": 3
  },
  {
    "id": 3,
    "title": "The Forest of Echoes",
    "description": "A mysterious forest that repeats your thoughts.",
    "status": "draft",
    "start_page_id": 5
  },
  {
    "id": 4,
    "title": "Chronicles of the Iron Kingdom",
    "description": "A medieval kingdom on the brink of war.",
    "status": "draft",
    "start_page_id": 7
  },
  {
    "id": 5,
    "title": "Cyber Runner",
    "description": "A hacker navigating a dystopian megacity.",
    "status": "published",
    "start_page_id": 9
  },
  {
    "id": 6,
    "title": "The Time Loop Café",
    "description": "A café where every day repeats.",
    "status": "draft",
    "start_page_id": 11
  },
  {
    "id": 7,
    "title": "Voyage of the Silver Whale",
    "description": "A fantasy adventure on a flying ship.",
    "status": "draft",
    "start_page_id": 13
  },
  {
    "id": 8,
    "title": "The Last Oracle",
    "description": "A world where prophecies are illegal.",
    "status": "published",
    "start_page_id": 15
  },
  {
    "id": 9,
    "title": "Underworld Delivery Service",
    "description": "A courier delivering packages to supernatural beings.",
    "status": "draft",
    "start_page_id": 17
  },
  {
    "id": 10,
    "title": "The Neon Tournament",
    "description": "A futuristic combat competition.",
    "status": "published",
    "start_page_id": 19
  }
]
📌 2. PAGES (IDs 1–20)
Each story gets 2 pages (1 normal + 1 ending).
This keeps everything clean and predictable.

json
[
  { "id": 1, "story_id": 1, "text": "You wake up in a ruined temple.", "is_ending": false, "ending_label": null },
  { "id": 2, "story_id": 1, "text": "A shadowy figure steals the amulet.", "is_ending": true, "ending_label": "Bad Ending" },

  { "id": 3, "story_id": 2, "text": "Alarms blare across Solaris Station.", "is_ending": false, "ending_label": null },
  { "id": 4, "story_id": 2, "text": "You escape in a damaged pod.", "is_ending": true, "ending_label": "Survivor Ending" },

  { "id": 5, "story_id": 3, "text": "Whispers echo your name.", "is_ending": false, "ending_label": null },
  { "id": 6, "story_id": 3, "text": "You merge with the forest.", "is_ending": true, "ending_label": "Spirit Ending" },

  { "id": 7, "story_id": 4, "text": "The king summons you.", "is_ending": false, "ending_label": null },
  { "id": 8, "story_id": 4, "text": "The kingdom falls to invaders.", "is_ending": true, "ending_label": "Defeat Ending" },

  { "id": 9, "story_id": 5, "text": "Drones scan the neon streets.", "is_ending": false, "ending_label": null },
  { "id": 10, "story_id": 5, "text": "You hack the central AI.", "is_ending": true, "ending_label": "Revolution Ending" },

  { "id": 11, "story_id": 6, "text": "The café clock resets again.", "is_ending": false, "ending_label": null },
  { "id": 12, "story_id": 6, "text": "You break the time loop.", "is_ending": true, "ending_label": "Freedom Ending" },

  { "id": 13, "story_id": 7, "text": "The Silver Whale takes flight.", "is_ending": false, "ending_label": null },
  { "id": 14, "story_id": 7, "text": "The ship crashes into a storm.", "is_ending": true, "ending_label": "Storm Ending" },

  { "id": 15, "story_id": 8, "text": "The Oracle whispers forbidden truths.", "is_ending": false, "ending_label": null },
  { "id": 16, "story_id": 8, "text": "You become the last Oracle.", "is_ending": true, "ending_label": "Ascension Ending" },

  { "id": 17, "story_id": 9, "text": "A demon requests a delivery.", "is_ending": false, "ending_label": null },
  { "id": 18, "story_id": 9, "text": "You deliver the package safely.", "is_ending": true, "ending_label": "Courier Ending" },

  { "id": 19, "story_id": 10, "text": "The arena lights ignite.", "is_ending": false, "ending_label": null },
  { "id": 20, "story_id": 10, "text": "You win the Neon Tournament.", "is_ending": true, "ending_label": "Champion Ending" }
]
📌 3. CHOICES (IDs 1–20)
Each non‑ending page gets 2 choices leading to its ending page.

json
[
  { "id": 1, "page_id": 1, "text": "Search the temple", "next_page_id": 2 },
  { "id": 2, "page_id": 1, "text": "Follow the footsteps", "next_page_id": 2 },

  { "id": 3, "page_id": 3, "text": "Run to engineering", "next_page_id": 4 },
  { "id": 4, "page_id": 3, "text": "Head to escape pods", "next_page_id": 4 },

  { "id": 5, "page_id": 5, "text": "Enter deeper", "next_page_id": 6 },
  { "id": 6, "page_id": 5, "text": "Retreat", "next_page_id": 6 },

  { "id": 7, "page_id": 7, "text": "Accept mission", "next_page_id": 8 },
  { "id": 8, "page_id": 7, "text": "Refuse", "next_page_id": 8 },

  { "id": 9, "page_id": 9, "text": "Hack drones", "next_page_id": 10 },
  { "id": 10, "page_id": 9, "text": "Hide", "next_page_id": 10 },

  { "id": 11, "page_id": 11, "text": "Talk to barista", "next_page_id": 12 },
  { "id": 12, "page_id": 11, "text": "Inspect clock", "next_page_id": 12 },

  { "id": 13, "page_id": 13, "text": "Take the helm", "next_page_id": 14 },
  { "id": 14, "page_id": 13, "text": "Explore the deck", "next_page_id": 14 },

  { "id": 15, "page_id": 15, "text": "Listen closely", "next_page_id": 16 },
  { "id": 16, "page_id": 15, "text": "Ignore the voice", "next_page_id": 16 },

  { "id": 17, "page_id": 17, "text": "Accept delivery", "next_page_id": 18 },
  { "id": 18, "page_id": 17, "text": "Decline", "next_page_id": 18 },

  { "id": 19, "page_id": 19, "text": "Enter the arena", "next_page_id": 20 },
  { "id": 20, "page_id": 19, "text": "Prepare strategy", "next_page_id": 20 }
]
🎁 If you want, I can also generate:
✔ A full Postman Collection (.json)
With folders (Stories / Pages / Choices)

With POST, GET, PUT, DELETE

With example bodies already filled

With environment variables ({{base_url}})

Just say “Generate the Postman collection” and I’ll prepare it cleanly for import.


Alright Tatchi, let’s fix this cleanly.

You’re getting:

405 METHOD NOT ALLOWED  
→ This means your Flask backend does NOT allow POST on /stories.

This has nothing to do with Postman or your JSON.
Your JSON is fine.
The backend route is the problem.

Let’s walk through this in a structured way so you can fix it in minutes.

✅ Why You’re Getting 405
A 405 error means:

The route exists but not for that HTTP method,
OR

The route exists but only accepts GET, not POST.

Example:

python
@app.route('/stories')
def get_stories():
    ...
This route only accepts GET, so POST → 405.

✅ How to Fix It (Add POST Route)
You need something like this in your Flask app:

python
@app.route('/stories', methods=['POST'])
def create_story():
    data = request.get_json()

    new_story = Story(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'draft'),
        start_page_id=data.get('start_page_id')
    )

    db.session.add(new_story)
    db.session.commit()

    return jsonify({"message": "Story created", "story": {
        "id": new_story.id,
        "title": new_story.title,
        "description": new_story.description,
        "status": new_story.status,
        "start_page_id": new_story.start_page_id
    }}), 201
Make sure:

✔ You imported:
python
from flask import request, jsonify
✔ Your model is imported
✔ Your database is initialized
✔ The route is inside the same file or blueprint
✅ Confirm Your Routes
Run:

bash
flask routes
You should see something like:

Code
/stories  GET, POST
/stories/<id>  GET, PUT, DELETE
If POST is missing → your route is not defined.

🧪 Test With This Postman Body
Use this clean JSON:

json
{
  "title": "Voyage of the Silver Whale",
  "description": "A fantasy adventure on a flying ship.",
  "status": "draft",
  "start_page_id": 13
}
⚠️ Remove "id": 7  
You never send IDs when creating new items — the database generates them.

🔍 If you want, I can also:
Review your entire Flask API file

Generate a full CRUD structure for Stories, Pages, Choices

Build a Postman collection you can import

Help you fix the JSONDecodeError in your other tab

Just tell me “check my Flask file” and paste it here.

create a readme file :https://chat.mistral.ai/chat/9c181218-caff-46fb-8b3a-c0fb240d2873
Absolutely, Tatchi — I can craft a clean, professional README.md for your Django–Flask project.
Since you didn’t provide the repo content directly, I’ll create a well‑structured, modern, developer‑friendly README that fits the architecture you’ve been building:

Flask API (Stories, Pages, Choices)

Django frontend (or second service)

Postman usage

Setup instructions

Project goals (Python Web Dev final project)

You can paste this directly into your GitHub repo.

📄 README.md — Django–Flask Project
markdown
# Django–Flask Interactive Story Project

This project is a full‑stack web application combining **Flask (backend API)** and **Django (frontend interface)** to create and manage interactive branching stories.  
It was developed as part of the **Python for Web Development Final Project**.

---

## 🚀 Project Overview

The application allows users to:

- Create stories  
- Add pages to each story  
- Add choices that connect pages  
- Build branching narrative structures  
- Interact with the story through a clean UI (Django)  
- Manage data through a REST API (Flask)

The backend exposes a structured API for Stories, Pages, and Choices, while the frontend consumes this API to display and navigate interactive stories.

---

## 🧱 Project Architecture

/Django-Flask-Project
│
├── flask_api/           # Flask backend (REST API)
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   ├── database.db
│   └── requirements.txt
│
├── django_frontend/     # Django frontend (UI)
│   ├── templates/
│   ├── static/
│   ├── views.py
│   ├── urls.py
│   └── settings.py
│
└── README.md



---

## 🧩 Flask API Structure

### **Story Model**
- `id`
- `title`
- `description`
- `status` (draft, published, suspended)
- `start_page_id`

### **Page Model**
- `id`
- `story_id`
- `text`
- `is_ending`
- `ending_label`

### **Choice Model**
- `id`
- `page_id`
- `text`
- `next_page_id`

---

## 🔌 API Endpoints

### **Stories**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stories` | Get all stories |
| GET | `/stories/<id>` | Get a specific story |
| POST | `/stories` | Create a new story |
| PUT | `/stories/<id>` | Update a story |
| DELETE | `/stories/<id>` | Delete a story |

### **Pages**
| Method | Endpoint |
|--------|----------|
| GET | `/pages` |
| POST | `/pages` |
| PUT | `/pages/<id>` |
| DELETE | `/pages/<id>` |

### **Choices**
| Method | Endpoint |
|--------|----------|
| GET | `/choices` |
| POST | `/choices` |
| PUT | `/choices/<id>` |
| DELETE | `/choices/<id>` |

---

## 🧪 Testing With Postman

A full Postman collection is included (or can be generated on request).  
You can test:

- Creating stories  
- Adding pages  
- Linking choices  
- Navigating story branches  

Example POST body for creating a story:

```json
{
  "title": "Voyage of the Silver Whale",
  "description": "A fantasy adventure on a flying ship.",
  "status": "draft",
  "start_page_id": 13
}


⚙️ Installation & Setup
1. Clone the repository
bash
git clone https://github.com/TATCHIwillyjunior/Django-Flask-Project
cd Django-Flask-Project
🐍 Flask Backend Setup
Create virtual environment
bash
cd flask_api
python3 -m venv venv
source venv/bin/activate
Install dependencies
bash
pip install -r requirements.txt
Run the API
bash
flask run
API runs at:

Code
http://127.0.0.1:5000
🎨 Django Frontend Setup
Install dependencies
bash
cd django_frontend
pip install -r requirements.txt
Run Django server
bash
python manage.py runserver
Frontend runs at:

Code
http://127.0.0.1:8000
🧭 How the System Works
Create a Story

Add Pages to the story

Mark some pages as endings

Add Choices that connect pages

Django frontend displays the story and lets users navigate choices

Flask API stores and manages all data