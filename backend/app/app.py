from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.app_context()

CORS(app)

# Initialize Azure Cosmos DB
# CosmosDB.init_app(app)
mongo = MongoClient(app.config['MONGO_DB_URI'])
db = mongo[app.config['MONGO_DB_NAME']]

def create_app():
    from routes.user import user_bp
    from routes.folder import folder_bp
    from routes.browsing_history import browsing_history_bp
    from routes.downloads import downloads_bp

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(folder_bp, url_prefix='/folders')
    app.register_blueprint(browsing_history_bp, url_prefix='/browsing_history')
    app.register_blueprint(downloads_bp, url_prefix='/downloads')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
