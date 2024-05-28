from flask import Blueprint, request, jsonify
from services.folder import FolderService

folder_bp = Blueprint('folders', __name__)
folder_service = FolderService()

# folders
@folder_bp.route('/', methods=['POST'])
def add_folder():
    data = request.json
    folder = folder_service.create_folder(data['name'], data['summary'])
    return jsonify(folder.to_dict()), 201

@folder_bp.route('/all', methods=['GET'])
def get_folders():
    return jsonify(folder_service.get_folders())

@folder_bp.route('/<folder_name>', methods=['GET'])
def get_folder(folder_name):
    return jsonify(folder_service.get_folder_by_name(folder_name))

# folder web_urls
@folder_bp.route('/<folder_name>/web_urls', methods=['GET'])
def get_folder_web_urls(folder_name):
    return jsonify(folder_service.get_web_urls(folder_name))

@folder_bp.route('/<folder_name>/web_urls/add', methods=['PUT'])
def add_folder_web_urls(folder_name):
    data = request.json
    return jsonify(folder_service.add_web_urls(folder_name, data['web_urls']))

@folder_bp.route('/<folder_name>/web_urls/delete', methods=['PUT'])
def delete_folder_web_urls(folder_name):
    data = request.json
    return jsonify(folder_service.delete_web_urls(folder_name, data['web_urls'])) 

# folder image_urls
@folder_bp.route('/<folder_name>/image_urls', methods=['GET'])
def get_folder_image_urls(folder_name):
    return jsonify(folder_service.get_image_urls(folder_name))

@folder_bp.route('/<folder_name>/image_urls/add', methods=['PUT'])
def add_folder_image_urls(folder_name):
    data = request.json
    return jsonify(folder_service.add_image_urls(folder_name, data['image_urls']))

@folder_bp.route('/<folder_name>/image_urls/delete', methods=['PUT'])
def delete_folder_image_urls(folder_name):
    data = request.json
    return jsonify(folder_service.delete_image_urls(folder_name, data['image_urls'])) 

# folder download_urls
@folder_bp.route('/<folder_name>/download_urls', methods=['GET'])
def get_folder_download_urls(folder_name):
    return jsonify(folder_service.get_download_urls(folder_name))

@folder_bp.route('/<folder_name>/download_urls/add', methods=['PUT'])
def add_folder_download_urls(folder_name):
    data = request.json
    return jsonify(folder_service.add_download_urls(folder_name, data['download_urls']))

@folder_bp.route('/<folder_name>/download_urls/delete', methods=['PUT'])
def delete_folder_download_urls(folder_name):
    data = request.json
    return jsonify(folder_service.delete_download_urls(folder_name, data['download_urls'])) 
