import os
from flask import Flask, Response, request, jsonify
from pymongo import MongoClient
from config import Config
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.app_context()
cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.secret_key = app.config["GOOGLE_SECRET_KEY"]
mongo = MongoClient(app.config['MONGO_DB_URI'])
db = mongo[app.config['MONGO_DB_NAME']]

def create_app():
    from routes.user import user_bp
    from routes.folder import folder_bp
    from routes.browsing_history import browsing_history_bp
    from routes.downloads import downloads_bp
    from routes.search import search_bp
    from routes.oauth import oauth_bp

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(folder_bp, url_prefix='/folders')
    app.register_blueprint(browsing_history_bp, url_prefix='/browsing_history')
    app.register_blueprint(downloads_bp, url_prefix='/downloads')
    app.register_blueprint(search_bp, url_prefix='/search')
    app.register_blueprint(oauth_bp, url_prefix='/oauth')

    return app


@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
