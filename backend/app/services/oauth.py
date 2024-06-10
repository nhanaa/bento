import os
import jwt
import datetime
from flask_cors import CORS
from flask import Flask, redirect, request, session, jsonify
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
from services.user import UserService
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("GOOGLE_SECRET_KEY")
CORS(app, supports_credentials=True)
userService = UserService()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_AUTH_URL = "http://127.0.0.1:5000/oauth/google/callback"
GOOGLE_SECRET_JSON_PATH = os.getenv("GOOGLE_CLIENT_SECRET_JSON")
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email', 'openid']

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # This line allows the use of http instead of https for OAuth

class OAuthService:
    google_flow = Flow.from_client_secrets_file(
        GOOGLE_SECRET_JSON_PATH,
        scopes=SCOPES,
        redirect_uri=GOOGLE_AUTH_URL
    )

    @staticmethod
    def create_token(user_info):
        name = str(user_info.get('name', ''))
        email = str(user_info.get('email', ''))
        print(f"SECRET_KEY: {app.secret_key}, Type: {type(app.secret_key)}")
        payload = {
            'name': name,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
        }
        payload['exp'] = int(payload['exp'].timestamp())
        try:
            token = jwt.encode(payload, app.secret_key, algorithm='HS256')
            print(f"Generated Token: {token}")  # Debugging line
            return token
        except Exception as e:
            print(f"Error during token encoding: {e}")  # Debugging line
            raise e

    @staticmethod
    def google_login():
        try:
            authorization_url, state = OAuthService.google_flow.authorization_url(access_type='offline', prompt='select_account')
            session['state'] = state
            session.modified = True  # Ensure the session is saved
            print(f"Authorization URL: {authorization_url}")  # Debugging line
            return redirect(authorization_url)
        except Exception as e:
            print(f"Error during Google login: {e}")  # Debugging line
            return str(e), 500

    @staticmethod
    def google_callback():
        try:
            OAuthService.google_flow.fetch_token(authorization_response=request.url)
            credentials = OAuthService.google_flow.credentials
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            user = userService.get_user_by_email(user_info['email'])
            if not user:
                user, _ = userService.create_user(user_info["email"], user_info['name'])
            
            # Convert datetime objects to strings
            user_serializable = {
                "email": user["email"],
                "name": user["name"],
                "created_at": user["created_at"].isoformat() if isinstance(user["created_at"], datetime.datetime) else user["created_at"],
                "updated_at": user["updated_at"].isoformat() if isinstance(user["updated_at"], datetime.datetime) else user["updated_at"]
            }
            
            token = OAuthService.create_token(user_info)
            user_json = json.dumps(user_serializable)
            react_app_url = f"http://localhost:5173/auth?token={token}&user={user_json}"
            return redirect(react_app_url)
        except Exception as e:
            return str(e), 500


    @staticmethod
    def logout():
        session.clear() 
        return jsonify({"message": "Logged out successfully"}), 200