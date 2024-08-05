from flask import Blueprint, request, jsonify
import firebase_admin
from firebase_admin import auth, firestore

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

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



@auth_bp.route('/user-profile', methods=['GET'])
def get_user_profile():
    id_token = request.headers.get('Authorization')

    if not id_token:
        return jsonify({'error': 'ID token is required.'}), 401

    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Retrieve user details from Firestore
        db = firestore.client()
        user_ref = db.collection('users').document(uid)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return jsonify({'error': 'User not found.'}), 404

        user_data = user_doc.to_dict()
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500