from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import tweepy
import os
from datetime import datetime, timedelta

# Setup Flask App
app = Flask(__name__)

# Configure PostgreSQL Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://twitterdb_i20j_user:XSWxgFSpBwEfGhwhPNd9ZLjKzhqD3iPa@dpg-crtveeggph6c73dd6q5g-a.oregon-postgres.render.com/twitterdb_i20j')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Setup Twitter API (using tweepy)
client = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

# Define a SQLAlchemy model for storing Tweets
class Tweet(db.Model):
    __tablename__ = 'tweets'
    
    id = db.Column(db.String(255), primary_key=True)  # Twitter ID
    username = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Tweet {self.id} by {self.username}>"

# Create the database tables (if they don't exist)
with app.app_context():
    db.create_all()

# Fetch and save tweets to the database
def fetch_and_save_tweets(username):
    try:
        # Check if tweets already exist in the database for the username
        existing_tweets = Tweet.query.filter_by(username=username).all()
        if existing_tweets:
            # Return cached tweets from the database
            tweet_data = [{'id': tweet.id, 'text': tweet.content, 'created_at': tweet.created_at} for tweet in existing_tweets]
            return tweet_data

        # Fetch tweets from Twitter API
        response = client.get_users_tweets(id=username, max_results=10)  # `username` here should be replaced with Twitter user_id
        if response.data:
            tweet_data = []
            for tweet in response.data:
                # Save the tweet to the database
                new_tweet = Tweet(id=tweet.id, username=username, content=tweet.text, created_at=datetime.utcnow())
                db.session.add(new_tweet)
                db.session.commit()

                tweet_data.append({'id': tweet.id, 'text': tweet.text, 'created_at': datetime.utcnow()})
            
            return tweet_data
        else:
            return {"error": "No tweets found"}

    except Exception as e:
        return {"error": str(e)}

# Route to fetch tweets for a user
@app.route('/tweets/<username>', methods=['GET'])
def fetch_tweets(username):
    tweets = fetch_and_save_tweets(username)
    return jsonify(tweets)

# Example route
@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Twitter Scraper API!'})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
