import firebase_admin 
from firebase_admin import auth, firestore
from flask import Blueprint, request, jsonify
from app.services.auth_service import login, create_user

auth_bp = Blueprint('auth', __name__)  
auth=firebase_admin.auth 

@auth_bp.route('/sign_up', methods=['POST'])    
def create_user():
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



@auth_bp.route('/login', methods=['POST'])
def login_route():
    auth = firebase_admin.auth
    data = request.json
    email = data.get('email', '')   
    password = data.get('password', '')
    user = login(email, password)
    print(f"login: {user}")
    # returns a dictionary with a key called 'idToken' which is the jwt token
    if user:
        return jsonify({'message': "User successfully logged in"}), 200
    else:
        return jsonify({'message': "Error logging in"}), 400

@auth_bp.route('/verify_id_token', methods=['POST'])
def verify_id_token():
    data = request.json
    idToken = data.get('idToken', '')
    print(idToken)
    decoded_token = auth.verify_id_token(idToken)
    uid = decoded_token['uid']
    print(f"decoded token {decoded_token}")
    return jsonify({"uid": uid, "status": "Token is valid"}), 200



