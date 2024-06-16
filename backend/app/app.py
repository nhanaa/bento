from flask import Flask
from utils.db import MongoDB
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.app_context()

def create_app():
    mongo = MongoDB.init_app(app)
    
    from routes.user import user_bp
    from routes.folder import folder_bp
    from routes.search import search_bp

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(folder_bp, url_prefix='/users/<user_id>/folders')
    app.register_blueprint(search_bp, url_prefix='/users/<user_id>/searches')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)