from flask import Blueprint, request, jsonify
from services.browsing_history import BrowsingHistoryService
from services.ai_services.link_rec import LinkRec

browsing_history_bp = Blueprint("browsing_history", __name__)
browsing_history_service = BrowsingHistoryService()
linkrec_service = LinkRec()

@browsing_history_bp.route("/", methods=["GET"])
def get_browsing_history_by_ip():
    data = request.json
    ip = data["ip"]
    browsing_history = browsing_history_service.get_browsing_history_by_ip(ip)
    if browsing_history == None:
        return jsonify({"error": "Browsing history not found"}), 404

    return jsonify(browsing_history)


@browsing_history_bp.route("/", methods=["POST"])
def send_browsing_history():
    data = request.json
    # clean up browsing history by ip
    browsing_history_service.clean_browsing_history_by_ip(data["ip"])

    if not data["browsing_history"]:
        return jsonify({"error": "Browsing history is empty"}), 400

    browsing_history = browsing_history_service.add_browsing_history(
        linkrec_service.embed_browsing_history(data["browsing_history"])
    )

    if not browsing_history:
        return jsonify({"error": "Failed to add browsing history"}), 400
    return jsonify(browsing_history), 201
