from flask import Blueprint, request, jsonify
from ..services.downloads import DownloadsService

downloads_bp = Blueprint('downloads_bp', __name__)
downloads_service = DownloadsService()

@downloads_bp.route('/', methods=['GET'])
def get_downloads_by_ip():
  data = request.json
  ip = data['ip']
  downloads = downloads_service.get_downloads_by_ip(ip)
  if downloads == None:
    return jsonify({"error": "Downloads not found"}), 404

  return jsonify(downloads)

@downloads_bp.route('/', methods=['POST'])
def send_downloads():
  data = request.json
  # clean up downloads by ip
  downloads_service.clean_downloads_by_ip(data['ip'])

  if not data['downloads']:
    return jsonify({"error": "Downloads are empty"}), 400

  downloads = downloads_service.add_downloads(data['downloads'])
  if not downloads:
    return jsonify({"error": "Failed to add downloads"}), 400
  return jsonify(downloads), 201
