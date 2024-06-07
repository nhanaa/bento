import os
from flask import Flask
from routes.user import user_bp
from routes.folder import folder_bp
# from routes.file import file_bp
from routes.oauth import oauth_bp

from utils.db import CosmosDB
from config import Config
from dotenv import load_dotenv



def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.secret_key = os.getenv("GOOGLE_SECRET_KEY")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'oauth_'
    app.config['SESSION_FILE_DIR'] = './flask_session/'
    # app.config.from_object(Config)

    # # Initialize Azure Cosmos DB
    # CosmosDB.init_app(app)

    # Register blueprints
    from routes.user import user_bp
    from routes.folder import folder_bp
    from routes.search import search_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(folder_bp, url_prefix='/folders')
    # app.register_blueprint(file_bp, url_prefix='/files')
    app.register_blueprint(oauth_bp, url_prefix="/oauth")
    app.register_blueprint(search_bp, url_prefix='/search')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)