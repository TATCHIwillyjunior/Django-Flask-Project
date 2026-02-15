from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound, BadRequest

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='draft')
    start_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    start_page = db.relationship('Page', foreign_keys=[start_page_id], post_update=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey('story.id'), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(100))
    story = db.relationship('Story', backref=db.backref('pages', lazy=True), foreign_keys=[story_id])

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page = db.relationship('Page', backref='choices', foreign_keys=[page_id])
    next_page = db.relationship('Page', foreign_keys=[next_page_id])

# Create tables
with app.app_context():
    db.create_all()

# Helper for error responses
def error_response(message, status_code=400):
    return jsonify({'error': message}), status_code

# Story Endpoints
@app.route('/stories', methods=['GET'])
def get_stories():
    status = request.args.get('status')
    query = request.args.get('q', '')

    stories = Story.query
    if status:
        stories = stories.filter_by(status=status)
    if query:
        stories = stories.filter(Story.title.ilike(f'%{query}%'))

    return jsonify([{
        'id': s.id,
        'title': s.title,
        'description': s.description,
        'status': s.status
    } for s in stories.all()])

@app.route('/stories/<int:id>', methods=['GET'])
def get_story(id):
    story = Story.query.get_or_404(id)
    return jsonify({
        'id': story.id,
        'title': story.title,
        'description': story.description,
        'status': story.status
    })

@app.route('/stories', methods=['POST'])
def create_story():
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return error_response('Title is required', 400)

        story = Story(
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', 'draft')
        )
        db.session.add(story)
        db.session.commit()

        return jsonify({
            'id': story.id,
            'title': story.title,
            'description': story.description,
            'status': story.status
        }), 201
    except Exception as e:
        return error_response(str(e))

@app.route('/stories/<int:id>', methods=['PUT'])
def update_story(id):
    try:
        story = Story.query.get_or_404(id)
        data = request.get_json()

        if 'title' in data:
            story.title = data['title']
        if 'description' in data:
            story.description = data['description']
        if 'status' in data:
            story.status = data['status']
        if 'start_page_id' in data:
            story.start_page_id = data['start_page_id']

        db.session.commit()

        return jsonify({
            'id': story.id,
            'title': story.title,
            'description': story.description,
            'status': story.status
        })
    except Exception as e:
        return error_response(str(e))

@app.route('/stories/<int:id>', methods=['DELETE'])
def delete_story(id):
    try:
        story = Story.query.get_or_404(id)
        db.session.delete(story)
        db.session.commit()
        return jsonify({'message': 'Story deleted successfully'}), 200
    except Exception as e:
        return error_response(str(e))

# Page Endpoints
@app.route('/stories/<int:story_id>/pages', methods=['POST'])
def create_page(story_id):
    try:
        story = Story.query.get_or_404(story_id)
        data = request.get_json()

        if not data or 'text' not in data:
            return error_response('Text is required', 400)

        page = Page(
            story_id=story_id,
            text=data['text'],
            is_ending=data.get('is_ending', False),
            ending_label=data.get('ending_label')
        )
        db.session.add(page)
        db.session.commit()

        return jsonify({
            'id': page.id,
            'story_id': page.story_id,
            'text': page.text,
            'is_ending': page.is_ending,
            'ending_label': page.ending_label
        }), 201
    except Exception as e:
        return error_response(str(e))

@app.route('/pages/<int:id>', methods=['GET'])
def get_page(id):
    page = Page.query.get_or_404(id)
    return jsonify({
        'id': page.id,
        'text': page.text,
        'is_ending': page.is_ending,
        'ending_label': page.ending_label,
        'choices': [{'id': c.id, 'text': c.text, 'next_page_id': c.next_page_id} for c in page.choices]
    })

@app.route('/pages/<int:id>', methods=['DELETE'])
def delete_page(id):
    try:
        page = Page.query.get_or_404(id)
        db.session.delete(page)
        db.session.commit()
        return jsonify({'message': 'Page deleted successfully'}), 200
    except Exception as e:
        return error_response(str(e))

# Choice Endpoints
@app.route('/pages/<int:page_id>/choices', methods=['POST'])
def create_choice(page_id):
    try:
        page = Page.query.get_or_404(page_id)
        data = request.get_json()

        if not data or 'text' not in data or 'next_page_id' not in data:
            return error_response('Text and next_page_id are required', 400)

        # Check if next_page exists
        next_page = Page.query.get(data['next_page_id'])
        if not next_page:
            return error_response('Next page does not exist', 400)

        choice = Choice(
            page_id=page_id,
            text=data['text'],
            next_page_id=data['next_page_id']
        )
        db.session.add(choice)
        db.session.commit()

        return jsonify({
            'id': choice.id,
            'page_id': choice.page_id,
            'text': choice.text,
            'next_page_id': choice.next_page_id
        }), 201
    except Exception as e:
        return error_response(str(e))

@app.route('/choices/<int:id>', methods=['DELETE'])
def delete_choice(id):
    try:
        choice = Choice.query.get_or_404(id)
        db.session.delete(choice)
        db.session.commit()
        return jsonify({'message': 'Choice deleted successfully'}), 200
    except Exception as e:
        return error_response(str(e))

# Start Page Endpoint
@app.route('/stories/<int:id>/start', methods=['GET'])
def get_start_page(id):
    story = Story.query.get_or_404(id)
    if not story.start_page_id:
        return error_response('No start page set for this story', 404)

    page = Page.query.get_or_404(story.start_page_id)
    return jsonify({
        'id': page.id,
        'text': page.text,
        'is_ending': page.is_ending,
        'ending_label': page.ending_label,
        'choices': [{'id': c.id, 'text': c.text, 'next_page_id': c.next_page_id} for c in page.choices]
    })

if __name__ == '__main__':
    app.run(debug=True)
