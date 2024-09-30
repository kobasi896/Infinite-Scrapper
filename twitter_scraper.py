import tweepy
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Twitter API credentials
API_KEY = os.getenv('API_KEY')
API_SECRET_KEY = os.getenv('API_SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Authentication with Twitter API
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Flask app initialization
app = Flask(__name__)

# PostgreSQL Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/twitterdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Tweet model for SQLAlchemy
class Tweet(db.Model):
    __tablename__ = 'tweets'
    
    id = db.Column(db.String(255), primary_key=True)  # Twitter's tweet ID
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet {self.id} by {self.username}>"

# Route to fetch tweets
@app.route('/tweets/<username>', methods=['GET'])
def fetch_tweets(username):
    try:
        # Check if tweets already exist in the database for the username
        existing_tweets = Tweet.query.filter_by(username=username).all()

        if existing_tweets:
            # Return the cached tweets from the database
            tweet_data = [{'id': tweet.id, 'text': tweet.content} for tweet in existing_tweets]
            return jsonify(tweet_data)

        # Fetch new tweets from Twitter API if no tweets found in the database
        response = client.get_users_tweets(username=username, max_results=10)

        if response.data:
            tweet_data = []
            for tweet in response.data:
                # Save the tweet to the database
                new_tweet = Tweet(id=tweet.id, username=username, content=tweet.text, created_at=datetime.utcnow())
                db.session.add(new_tweet)
                db.session.commit()

                tweet_data.append({'id': tweet.id, 'text': tweet.text})

            return jsonify(tweet_data)
        else:
            return jsonify({"error": "No tweets found"}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return "Welcome to Twitter Scraper API!"

if __name__ == "__main__":
    # Create database tables (if they don't already exist)
    with app.app_context():
        db.create_all()
    
    app.run(host="0.0.0.0", port=5000)

