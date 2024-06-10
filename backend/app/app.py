from flask import Flask
from pymongo import MongoClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.app_context()

# Initialize Azure Cosmos DB
# CosmosDB.init_app(app)
mongo = MongoClient(app.config['MONGO_DB_URI'])
db = mongo[app.config['MONGO_DB_NAME']]

def create_app():
    from routes.user import user_bp
    from routes.folder import folder_bp

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(folder_bp, url_prefix='/folders')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
