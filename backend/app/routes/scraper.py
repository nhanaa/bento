from flask import Blueprint, jsonify, request
from services.scraper import ScraperService

scraper_bp = Blueprint('scraper_bp', __name__)
scraper_service = ScraperService()

# testing
@scraper_bp.route('/', methods=['GET'])
def default():
    return 'Hello, user!'

@scraper_bp.route('/url/<url>', methods=['GET'])
def get_metadata(url):
    metadata = scraper_service.get_metadata(url)
    
    return jsonify(metadata)


