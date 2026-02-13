from flask import Blueprint, request, jsonify, current_app
from extensions import db
from model import Story, Page, Choice

api_bp = Blueprint("api", __name__)

def require_api_key():
    api_key = request.headers.get("X-API-KEY")
    if request.method in ["POST", "PUT", "DELETE"]:
        if api_key != current_app.config["API_KEY"]:
            return False
    return True

@api_bp.before_request
def check_api_key():
    if not require_api_key():
        return jsonify({"error": "Unauthorized"}), 401

# GET /stories?status=published
@api_bp.get("/stories")
def list_stories():
    status = request.args.get("status")
    q = Story.query
    if status:
        q = q.filter_by(status=status)
    stories = q.all()
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "description": s.description,
            "status": s.status,
            "start_page_id": s.start_page_id,
            "illustration_url": s.illustration_url,
        } for s in stories
    ])

# Implement:
# GET /stories/<id>
# GET /stories/<id>/start
# GET /pages/<id>
# POST /stories
# PUT /stories/<id>
# DELETE /stories/<id>
# POST /stories/<id>/pages
# POST /pages/<id>/choices
