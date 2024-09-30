from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import tweepy
import os
from datetime import datetime, timedelta

# Setup Flask App
app = Flask(__name__)

# Configure PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/twitterdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Setup Twitter API (using tweepy)
client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

# Model for storing tweets
class Tweet(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(280), nullable=False)  # Assuming tweet length constraint
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Fetch tweets and store them in the database
@app.route('/tweets/<username>', methods=['GET'])
def fetch_tweets(username):
    try:
        # Check if tweets were fetched within the last 60 seconds
        one_minute_ago = datetime.utcnow() - timedelta(seconds=60)
        recent_tweets = Tweet.query.filter(Tweet.username == username, Tweet.created_at >= one_minute_ago).all()

        if recent_tweets:
            # Return cached tweets from the database
            tweets = [{'id': tweet.id, 'text': tweet.content} for tweet in recent_tweets]
            return jsonify(tweets)
        else:
            # Fetch tweets from the Twitter API if no recent tweets are cached
            response = client.get_users_tweets(username=username, max_results=10)
            if response.data:
                tweets = []
                for tweet in response.data:
                    # Store new tweet in the database
                    new_tweet = Tweet(id=tweet.id, username=username, content=tweet.text, created_at=datetime.utcnow())
                    db.session.add(new_tweet)
                    db.session.commit()

                    tweets.append({'id': tweet.id, 'text': tweet.text})

                return jsonify(tweets)
            else:
                return jsonify({"error": "No tweets found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
