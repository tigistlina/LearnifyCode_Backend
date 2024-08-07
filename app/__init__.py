from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app, _apps, auth
import os
import base64
import tempfile
from dotenv import load_dotenv

load_dotenv()


def create_app(testing=False):
    app = Flask(__name__)

    # CORS configuration
    cors = CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:4200","https://learnify-frontend.netlify.app"],
            "allow_headers": ["accept", "accept-encoding", "authorization", "content-type", "dnt", "origin", "user-agent", "x-csrftoken", "x-requested-with"],
            "expose_headers": ["Authorization"],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "supports_credentials": True
        }
    })

    # Get Firestore project ID from environment variable
    firestore_project_id = os.getenv('FIREBASE_PROJECT_ID')
    firestore_emulator_host = os.getenv('FIRESTORE_EMULATOR_HOST')

    # Conditionally use Firestore emulator settings based on environment variable
    use_emulator = os.getenv('USE_FIRESTORE_EMULATOR','false').lower() == 'true'

    if testing or use_emulator:
        os.environ['FIRESTORE_EMULATOR_HOST'] = firestore_emulator_host
        os.environ['FIRESTORE_PROJECT_ID'] = firestore_project_id
        app.config['TESTING'] = True
    else:
        os.environ.pop('FIRESTORE_EMULATOR_HOST', None)
        os.environ.pop('FIRESTORE_PROJECT_ID', None)

    # Get the base64-encoded Firebase credentials from environment variables
    firebase_credentials_base64 = os.getenv('FIREBASE_CREDENTIALS_BASE64')

    if not firebase_credentials_base64:
        raise ValueError(
            "The base64-encoded Firebase credentials JSON is missing from environment variables.")

    # Decode the base64-encoded Firebase credentials and write them to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
        temp_file.write(base64.b64decode(firebase_credentials_base64))
        temp_file_path = temp_file.name

    # Initialize Firebase Admin SDK only if not already initialized
    if not _apps:
        cred = credentials.Certificate(temp_file_path)
        initialize_app(cred, {'projectId': firestore_project_id})

    app.db = firestore.client()

    # Import and register blueprints
    from .routes.lesson_routes import lesson_bp
    app.register_blueprint(lesson_bp)

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
