from flask import Blueprint, request, jsonify
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

@oauth_bp.route('/google/callback', methods=['GET', 'POST'])  # Allow both GET and POST
def google_callback():
    if request.method == 'POST':
        code = request.json.get('code')
        if code:
            return oauth_service.google_callback()
    return oauth_service.google_callback()

@oauth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return oauth_service.logout()
