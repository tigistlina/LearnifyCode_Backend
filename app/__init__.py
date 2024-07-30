from flask import Flask
from firebase_admin import credentials, firestore, initialize_app
import os


def create_app():
    app = Flask(__name__)

    # Get the path to the Firebase credentials JSON file from environment variables
    firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')

    if not firebase_credentials_path:
        raise ValueError(
            "The path to the Firebase credentials JSON file cannot be accessed.")

    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(firebase_credentials_path)
    initialize_app(cred)
    app.db = firestore.client()

    # Import and register blueprints
    from .routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp)

    return app
