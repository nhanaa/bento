from flask import Blueprint, request
from services.oauth import OAuthService

oauth_bp = Blueprint('oauth_bp', __name__)
oauth_service = OAuthService()

# testing
@oauth_bp.route('/', methods=['GET'])
def default():
    return 'Testing OAuth!'

@oauth_bp.route('/google/login', methods=['GET'])
def google_login():
    return oauth_service.google_login()

@oauth_bp.route('/google/callback', methods=['GET'])
def google_callback():
    return oauth_service.google_callback()

@oauth_bp.route('/github/login', methods=['GET'])
def github_login():
    return oauth_service.github_login()

@oauth_bp.route('/github/callback', methods=['GET'])
def github_callback():
    return oauth_service.github_callback()
