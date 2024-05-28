from flask import Flask
from routes.user import user_bp
from routes.folder import folder_bp
from routes.file import file_bp
from utils.db import CosmosDB
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Azure Cosmos DB
    CosmosDB.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(folder_bp, url_prefix='/folders')
    app.register_blueprint(file_bp, url_prefix='/files')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
