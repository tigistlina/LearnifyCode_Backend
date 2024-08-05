import firebase_admin
from firebase_admin import auth
import requests 
import os

def create_user(email, password):
    try:
        user = auth.create_user(
            email=email, 
            password=password
            )
        return {"uid": user.uid, "email": user.email}
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
        response = requests.post(url, data=payload)        
        # user = auth.get_user_by_email(email)
        # check if user email and password in database
        print(response.json())
        return(response.json().get("idToken"))
        # return user
    except Exception as e:
        print(f"Error logging in: {e}")
        return None     

# returns a dictionary with a key called 'idToken' which is the jwt token
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
    

