from extensions import db

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="draft")  # draft/published/suspended
    start_page_id = db.Column(db.Integer, nullable=True)
    illustration_url = db.Column(db.String(500), nullable=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_ending = db.Column(db.Boolean, default=False)
    ending_label = db.Column(db.String(200), nullable=True)
    illustration_url = db.Column(db.String(500), nullable=True)

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey("page.id"), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    next_page_id = db.Column(db.Integer, db.ForeignKey("page.id"), nullable=False)
