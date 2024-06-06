import os
from flask import Flask, redirect, request, session
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from requests_oauthlib import OAuth2Session

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

GOOGLE_SECRET_JSON_PATH = os.getenv("CLIENT_SECRET_JSON")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

class OAuthService:

    google_flow = Flow.from_client_secrets_file(
        GOOGLE_SECRET_JSON_PATH,
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
        redirect_uri='http://localhost:5000/google/callback'
    )

    @staticmethod
    def google_login():
        authorization_url, state = OAuthService.google_flow.authorization_url()
        session['state'] = state
        return redirect(authorization_url)

    @staticmethod
    def google_callback():
        OAuthService.google_flow.fetch_token(authorization_response=request.url)
        credentials = OAuthService.google_flow.credentials
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        return user_info

    @staticmethod
    def github_login():
        github = OAuth2Session(GITHUB_CLIENT_ID)
        authorization_url, state = github.authorization_url(authorization_base_url)
        session['oauth_state'] = state
        return redirect(authorization_url)

    @staticmethod
    def github_callback():
        github = OAuth2Session(GITHUB_CLIENT_ID, state=session['oauth_state'])
        github.fetch_token(token_url, client_secret=GITHUB_CLIENT_SECRET, authorization_response=request.url)
        user_info = github.get('https://api.github.com/user').json()
        return user_info
