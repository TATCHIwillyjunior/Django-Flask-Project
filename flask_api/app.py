from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stories.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models (as you provided)
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
    story = db.relationship('Story', backref='pages', foreign_keys=[story_id])

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey('page.id'), nullable=False)
    page = db.relationship('Page', backref='choices', foreign_keys=[page_id])

# Create tables
with app.app_context():
    db.create_all()

# API Endpoints
@app.route('/stories', methods=['GET'])
def get_stories():
    stories = Story.query.all()
    return jsonify([{'id': s.id, 'title': s.title, 'description': s.description} for s in stories])

@app.route('/stories/<int:id>', methods=['GET'])
def get_story(id):
    story = Story.query.get_or_404(id)
    return jsonify({'id': story.id, 'title': story.title, 'description': story.description, 'status': story.status})

@app.route('/stories/<int:id>/start', methods=['GET'])
def get_start_page(id):
    story = Story.query.get_or_404(id)
    page = Page.query.get_or_404(story.start_page_id)
    return jsonify({'id': page.id, 'text': page.text, 'is_ending': page.is_ending, 'choices': [{'id': c.id, 'text': c.text, 'next_page_id': c.next_page_id} for c in page.choices]})

@app.route('/pages/<int:id>', methods=['GET'])
def get_page(id):
    page = Page.query.get_or_404(id)
    return jsonify({'id': page.id, 'text': page.text, 'is_ending': page.is_ending, 'choices': [{'id': c.id, 'text': c.text, 'next_page_id': c.next_page_id} for c in page.choices]})

# GET /choices/<id> for Level 10/13/16 (not required for Level 7/10) - returns choice details including next_page_id
# @app.route('/pages/<int:page_id>/choices', methods=['GET'])
# def get_page_choices(page_id):
#     page = Page.query.get_or_404(page_id)
#     choices = Choice.query.filter_by(page_id=page_id).all()
#     return jsonify([{'id': c.id, 'page_id': c.page_id, 'text': c.text, 'next_page_id': c.next_page_id} for c in choices])

# @app.route('/choices/<int:choice_id>', methods=['GET'])
# def get_choice(choice_id):
#     choice = Choice.query.get_or_404(choice_id)
#     return jsonify({'id': choice.id, 'page_id': choice.page_id, 'text': choice.text, 'next_page_id': choice.next_page_id})

# @app.route('/choices', methods=['GET'])
# def get_all_choices():
#     choices = Choice.query.all()
#     return jsonify([{'id': c.id, 'page_id': c.page_id, 'text': c.text, 'next_page_id': c.next_page_id} for c in choices])

# Writing endpoints (for Level 10/13/16)

@app.route('/stories', methods=['POST'])
def create_story():
    data = request.get_json()
    
    # Handle both single object and list of objects
    if not isinstance(data, list):
        data = [data]
    
    created_stories = []
    for item in data:
        story = Story(
            title=item['title'], 
            description=item.get('description', ''), 
            status=item.get('status', 'draft'),
            start_page_id=item.get('start_page_id')
        )
        db.session.add(story)
        db.session.flush()  # Get the auto-generated ID
        created_stories.append({
            'id': story.id,
            'title': story.title,
            'description': story.description,
            'status': story.status,
            'start_page_id': story.start_page_id
        })
    
    db.session.commit()
    return jsonify(created_stories), 201

@app.route('/stories/<int:id>', methods=['PUT'])
def update_story(id):
    story = Story.query.get_or_404(id)
    data = request.get_json()
    story.title = data.get('title', story.title)
    story.description = data.get('description', story.description)
    story.status = data.get('status', story.status)
    story.start_page_id = data.get('start_page_id', story.start_page_id)
    db.session.commit()
    return jsonify({'id': story.id, 'title': story.title, 'description': story.description, 'status': story.status})

@app.route('/stories/<int:id>', methods=['DELETE'])
def delete_story(id):
    story = Story.query.get_or_404(id)
    db.session.delete(story)
    db.session.commit()
    return jsonify({'message': 'Story deleted'}), 200
# 
# DElete all stories (for testing purposes)
# @app.route('/stories', methods=['DELETE'])
# def delete_all_stories():
#     count = Story.query.delete()
#     db.session.commit()
#     return jsonify({'message': f'{count} stories deleted'}), 200

@app.route('/stories/<int:story_id>/pages', methods=['POST'])
def create_page(story_id):
    data = request.get_json()
    if isinstance(data, list):
        data = data[0] if data else {}
    page = Page(story_id=story_id, text=data['text'], is_ending=data.get('is_ending', False), ending_label=data.get('ending_label'))
    db.session.add(page)
    db.session.commit()
    return jsonify({'id': page.id, 'story_id': page.story_id, 'text': page.text, 'is_ending': page.is_ending, 'ending_label': page.ending_label}), 201

@app.route('/pages/<int:page_id>/choices', methods=['POST'])
def create_choice(page_id):
    data = request.get_json()
    if isinstance(data, list):
        data = data[0] if data else {}
    choice = Choice(page_id=page_id, text=data['text'], next_page_id=data['next_page_id'])
    db.session.add(choice)
    db.session.commit()
    return jsonify({'id': choice.id, 'page_id': choice.page_id, 'text': choice.text, 'next_page_id': choice.next_page_id}), 201


# Delete all pages for a story (for testing purposes)
# @app.route('/pages/<int:page_id>/choices', methods=['DELETE'])
# def delete_page_choices(page_id):
#     count = Choice.query.filter_by(page_id=page_id).delete()
#     db.session.commit()
#     return jsonify({'message': f'{count} choices deleted'}), 200

# @app.route('/choices/<int:choice_id>', methods=['DELETE'])
# def delete_choice(choice_id):
#     choice = Choice.query.get_or_404(choice_id)
#     db.session.delete(choice)
#     db.session.commit()
#     return jsonify({'message': 'Choice deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
