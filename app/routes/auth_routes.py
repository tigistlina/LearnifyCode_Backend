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
    
@auth_bp.route('/sign_up', methods=['POST'])
def create_user_route():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user_name = data.get('user_name')

    if not email or not password or not user_name:
        return jsonify({'error': 'Email, password, and name are required.'}), 400

    try:
        # Create user with Firebase Authentication
        user = auth.create_user(email=email, password=password)

        # Store additional user details in Firestore
        db = firestore.client()
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'email': email,
            'user_name': user_name,
            'uid': user.uid
        })

        return jsonify({'message': 'User created successfully', 'user_id': user.uid}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)


