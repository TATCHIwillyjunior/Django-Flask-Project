
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

json
{
  "title": "Voyage of the Silver Whale",
  "description": "A fantasy adventure on a flying ship.",
  "status": "draft",
  "start_page_id": 13
}


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






