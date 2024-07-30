from flask import Flask
from firebase_admin import credentials, firestore, initialize_app, _apps
import os

def create_app(testing=False):
    app = Flask(__name__)

    # Conditionally use Firestore emulator settings
    if testing:
        os.environ['FIRESTORE_EMULATOR_HOST'] = 'localhost:8080'
        os.environ['FIRESTORE_PROJECT_ID'] = 'learnify code'
        app.config['TESTING'] = True

    # Get the path to the Firebase credentials JSON file from environment variables
    firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')

    if not firebase_credentials_path:
        raise ValueError("The path to the Firebase credentials JSON file cannot be accessed.")

    # Initialize Firebase Admin SDK only if not already initialized
    if not _apps:
        cred = credentials.Certificate(firebase_credentials_path)
        initialize_app(cred)

    app.db = firestore.client()

    # Import and register blueprints
    from .routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp)

    return app
