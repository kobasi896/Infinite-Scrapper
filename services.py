from tweepy import Client
from datetime import datetime
from config import Config
from models import Tweet, db

client = Client(bearer_token=Config.BEARER_TOKEN)

def fetch_user_id(username):
    """Fetch the Twitter user ID from the username."""
    try:
        user_response = client.get_user(username=username)
        if user_response.data:
            return user_response.data.id
        else:
            return None
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return None

def fetch_and_save_tweets(username):
    """Fetch tweets for a username and save them to the database."""
    user_id = fetch_user_id(username)
    if not user_id:
        return {"error": "User not found"}

    # Check if tweets already exist in the database for the username
    existing_tweets = Tweet.query.filter_by(username=username).all()
    if existing_tweets:
        # Return cached tweets from the database
        return [
            {'id': tweet.id, 'text': tweet.content, 'created_at': tweet.created_at}
            for tweet in existing_tweets
        ]

    try:
        # Fetch tweets from Twitter API using the user ID
        response = client.get_users_tweets(
            id=user_id, max_results=10, tweet_fields=["created_at", "text"]
        )
        if response.data:
            tweet_data = []
            for tweet in response.data:
                # Save the tweet to the database
                new_tweet = Tweet(
                    id=str(tweet.id),
                    username=username,
                    content=tweet.text,
                    created_at=datetime.utcnow()
                )
                db.session.add(new_tweet)
                tweet_data.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at
                })

            db.session.commit()
            return tweet_data
        else:
            return {"error": "No tweets found"}

    except Exception as e:
        print(f"Error fetching tweets: {e}")
        return {"error": str(e)}
