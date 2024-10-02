from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Tweet(db.Model):
    """SQLAlchemy model for storing Tweets."""
    __tablename__ = 'tweets'

    id = db.Column(db.String(255), primary_key=True)  # Twitter ID
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet {self.id} by {self.username}>"
