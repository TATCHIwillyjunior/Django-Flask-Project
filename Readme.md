
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

''''json
{
  "title": "Voyage of the Silver Whale",
  "description": "A fantasy adventure on a flying ship.",
  "status": "draft",
  "start_page_id": 13
}'''

## 🔐 Level 16 — Authentication, Roles & Permissions -->
Level 16 introduces user accounts, role‑based permissions, story moderation, and API security.
This section describes how these features are implemented in the Django–Flask architecture.

## 👤 User Accounts (Django Authentication)
The project now supports:

User registration

Login / Logout

Password hashing

Session management

Implemented using Django’s built‑in authentication system.

Registration Fields
username

email

password

role (Reader or Author)

## 🧑‍💼 User Roles
Each user has a Profile with a role:

Role	Description
Reader (default)	Can play published stories and view their own play history
Author	Can create, edit, and delete their own stories
Admin (is_staff=True)	Can moderate stories and view global stats
Roles are stored in the Profile model and automatically created when a user is created.

## 🔒 Role‑Based Permissions
✔ Readers
Can browse published stories

Can play stories

Can view only their own play history

Cannot access author tools

✔ Authors
Can create stories

Can edit/delete only their own stories

Cannot suspend stories

✔ Admins
Can suspend stories

Can view global statistics

Can access Django admin panel

Author‑only views are protected using a custom decorator:

python
@author_required
Admin‑only actions use:

python
@staff_member_required

## 📊 Play Tracking (Updated for Level 16)
The Play model now includes:

python
user = models.ForeignKey(User, on_delete=models.CASCADE)
This means:

Every completed ending is linked to the logged‑in user

Readers only see their own plays

Authors/admins see global stats

Story‑specific and global statistics are filtered based on user role.

## 🚫 Story Moderation (Admin Only)
Admins can suspend a story:

Suspended stories are hidden from the public list

Suspended stories cannot be played

Authors cannot unsuspend their own stories

Suspension is performed via a PUT request to the Flask API:

json
{ "status": "suspended" }
## 🔑 Flask API Security (Mandatory for Level 16)
All write operations (POST, PUT, DELETE) in Flask are now protected by an API key.

Django sends:
Code
X-API-KEY: <secret>
Flask validates:
python
if request.headers.get("X-API-KEY") != API_KEY:
    return jsonify({"error": "Invalid API key"}), 401
Public endpoints (GET) remain open:
/stories

/stories/<id>

/pages/<id>

This ensures that only the Django frontend can modify story data.

## 🧭 Updated System Workflow (Level 16)
User logs in (Reader / Author / Admin)

Reader can:

Play published stories

Resume progress (auto‑save)

View their own stats

Author can:

Create/edit/delete their own stories

Preview draft stories

Admin can:

Suspend stories

View global stats

Django sends authenticated write requests to Flask using the API key

Flask validates the key before modifying data

## 🧪 Level 16 Test Checklist
Use this to verify your implementation:

Authentication
Register reader/author accounts

Login/logout works

Permissions
Reader cannot access author tools

Author cannot edit another author’s story

Admin can suspend stories

API Security
Flask rejects write requests without API key

Django sends API key correctly

Stats
Reader sees only their own plays

Author/admin sees global stats

Story‑specific stats display correctly

Moderation
Suspended stories disappear from public list

Suspended stories cannot be played

## ⚙️ Installation & Setup
1. Clone the repository
bash
git clone https://github.com/TATCHIwillyjunior/Django-Flask-Project
cd Django-Flask-Project


## 🐍 Flask Backend Setup

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


## 🎨 Django Frontend Setup
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


## 🧭 How the System Works
Create a Story

Add Pages to the story

Mark some pages as endings

Add Choices that connect pages

Django frontend displays the story and lets users navigate choices

Flask API stores and manages all data






