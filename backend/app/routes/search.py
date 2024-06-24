from flask import Blueprint, request, jsonify

from services.search import SearchService

search_bp = Blueprint('search_bp', __name__)
search_service = SearchService()

@search_bp.route('/', methods=['GET'])
def search():
    query = request.args.get('q')
    res = search_service.search(query)
    print(111, res)
    return jsonify(res), 200