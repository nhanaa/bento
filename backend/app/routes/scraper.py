from flask import Blueprint, request, jsonify
from services.scraper import ScraperService

scraper_bp = Blueprint('scraper_bp', __name__)
scraper_service = ScraperService()

@scraper_bp.route('/url/<url>', methods=['GET'])
def get_metadata(url):
    metadata = scraper_service.get_metadata(url)
    return jsonify(metadata)
