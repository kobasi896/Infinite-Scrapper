from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup Flask App
app = Flask(__name__)

# Configure PostgreSQL Database URI from .env file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
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

# Function to fetch the user ID from the username
def fetch_user_id(username):
    try:
        # Fetch user details to get the Twitter user ID
        user_response = client.get_user(username=username)
        if user_response.data:
            return user_response.data.id  # Return the user ID
        else:
            return None
    except Exception as e:
        return None

# Function to fetch tweets and save them to the database
def fetch_and_save_tweets(username):
    try:
        # First fetch the user ID using the username (Twitter handle)
        user_id = fetch_user_id(username)
        if not user_id:
            return {"error": "User not found"}

        # Check if tweets already exist in the database for the username
        existing_tweets = Tweet.query.filter_by(username=username).all()
        if existing_tweets:
            # Return cached tweets from the database
            tweet_data = [{'id': tweet.id, 'text': tweet.content, 'created_at': tweet.created_at} for tweet in existing_tweets]
            return tweet_data

        # Fetch tweets from Twitter API using the user ID
        response = client.get_users_tweets(id=user_id, max_results=10)
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

# Route for the front-end form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        tweets = fetch_and_save_tweets(username)
        return render_template('index.html', tweets=tweets, username=username)
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
