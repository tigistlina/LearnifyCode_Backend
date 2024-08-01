from flask import Flask
from firebase_admin import credentials, firestore, initialize_app, _apps
import os
from dotenv import load_dotenv

load_dotenv()

def create_app(testing=False):
    app = Flask(__name__)

    # Get Firestore project ID from environment variable
    firestore_project_id = os.getenv('FIRESTORE_PROJECT_ID')
    firestore_emulator_host = os.getenv('FIRESTORE_EMULATOR_HOST')

    # Conditionally use Firestore emulator settings based on environment variable
    use_emulator = os.getenv('USE_FIRESTORE_EMULATOR', 'false').lower() == 'true'

    if testing or use_emulator:
        os.environ['FIRESTORE_EMULATOR_HOST'] = firestore_emulator_host
        os.environ['FIRESTORE_PROJECT_ID'] = firestore_project_id
        app.config['TESTING'] = True
    else:
        os.environ.pop('FIRESTORE_EMULATOR_HOST', None)
        os.environ.pop('FIRESTORE_PROJECT_ID', None)

    # Get the path to the Firebase credentials JSON file from environment variables
    firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')

    if not firebase_credentials_path:
        raise ValueError(
            "The path to the Firebase credentials JSON file cannot be accessed.")

    # Initialize Firebase Admin SDK only if not already initialized
    if not _apps:
        cred = credentials.Certificate(firebase_credentials_path)
        initialize_app(cred, {'projectId': firestore_project_id})

    app.db = firestore.client()

    # Import and register blueprints
    from .routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp)

    return app
