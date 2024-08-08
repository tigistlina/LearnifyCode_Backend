import firebase_admin
from firebase_admin import auth, firestore
import requests
import os
from flask import Flask, Blueprint, request, jsonify

app = Flask(__name__)

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app()

auth_bp = Blueprint('auth', __name__)

def create_user(name, email, password, avatar_url):
    try:
        user = auth.create_user(
            name=name,
            email=email,
            password=password,
            photo_url=avatar_url

        )
        
        return {"uid": user.uid, "name": user.name, "email": user.email, "avatar_url": user.photo_url}
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def login(email, password):
    try:
        url = os.getenv('FIREBASE_WEB_API_KEY')
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        print(response.json())
        return response.json().get("idToken")
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def verify_id_token(idToken):
    try:
        decoded_token = auth.verify_id_token(idToken, check_revoked=True)
        uid = decoded_token['uid']
        return {"uid": uid}
    except auth.ExpiredIdTokenError:
        print("Error verifying token: Expired ID token. Please re-enter your credentials.")
        return None
    except auth.InvalidIdTokenError:
        print("Error verifying token: Invalid ID token")
        return None
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    photo_url = data.get('avatar_url')

    if not email or not password or not name:
        return jsonify({'error': 'Email, password, and name are required.'}), 400

    try:
        # Create user with Firebase Authentication
        user = auth.create_user(email=email, password=password)

        # Store additional user details in Firestore
        db = firestore.client()
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'email': email,
            'name': name,
            'uid': user.uid
        })

        return jsonify({'message': 'User created successfully', 'user_id': user.uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login_route():
    data = request.json
    email = data.get('email', '')
    password = data.get('password', '')
    token = login(email, password)
    print(f"login: {token}")
    if token:
        return jsonify({'message': "User successfully logged in", 'idToken': token}), 200
    else:
        return jsonify({'message': "Error logging in"}), 400

@auth_bp.route('/verify_id_token', methods=['POST'])
def verify_id_token_route():
    data = request.json
    idToken = data.get('idToken', '')
    print(idToken)
    result = verify_id_token(idToken)
    if result:
        return jsonify({"uid": result['uid'], "status": "Token is valid"}), 200
    else:
        return jsonify({'error': "Token verification failed"}), 400
