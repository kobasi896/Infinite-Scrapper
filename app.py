from flask import Flask, render_template, request
from config import Config
from models import db
from services import fetch_and_save_tweets
from dotenv import load_dotenv

def create_app():
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            username = request.form['username']
            tweets = fetch_and_save_tweets(username)
            return render_template('index.html', tweets=tweets, username=username)
        return render_template('index.html')

    return app

if __name__ == '__main__':
    load_dotenv()  # Ensure environment variables are loaded when running the app directly
    app = create_app()
    app.run(debug=True)
