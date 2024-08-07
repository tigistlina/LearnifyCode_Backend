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

def create_user(name, email, password):
    try:
        user = auth.create_user(
            display_name=name,
            email=email,
            password=password
        )
        return {"uid": user.uid, "name": user.display_name, "email": user.email}
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
    

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)


