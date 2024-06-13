from flask import Blueprint, request, jsonify

from services.search import SearchService

search_bp = Blueprint('search_bp', __name__)
search_service = SearchService()

@search_bp.route('/<user_id>', methods=['GET'])
def search(user_id):
    query = request.args.get('q')
    res = search_service.search(user_id, query)
    return jsonify(res), 200