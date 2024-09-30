from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import tweepy
import os

# Setup Flask App
app = Flask(__name__)

# Configure PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/twitterdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Setup Twitter API (using tweepy)
client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

# Create the database tables (first run only)
with app.app_context():
    db.create_all()

# Example route
@app.route('/')
def index():
    # Example logic, replace this as needed
    return jsonify({'message': 'Hello, world!'})

if __name__ == '__main__':
    app.run(debug=True)
