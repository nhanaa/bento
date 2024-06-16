from flask import Blueprint, request, jsonify
from services.folder import FolderService

folder_bp = Blueprint('folders', __name__)
folder_service = FolderService()

# folders
@folder_bp.route('/', methods=['POST'])
def add_folder(user_id):
    data = request.json
    folder = folder_service.create_folder(data['folder_name'], data['summary'], user_id)
    return jsonify(folder.to_dict()), 201

@folder_bp.route('/', methods=['GET'])
def get_folders_by_user_id(user_id):
    return jsonify(folder_service.get_folders_by_user_id(user_id))

@folder_bp.route('/<folder_name>', methods=['GET'])
def get_folder(user_id, folder_name):
    folder = folder_service.get_folder_by_name(folder_name, user_id)
    if not folder:
        return None
    return jsonify(folder.to_dict())

# folder web_urls
@folder_bp.route('/<folder_name>/web_urls', methods=['GET'])
def get_folder_web_urls(user_id, folder_name):
    return jsonify(folder_service.get_web_urls(folder_name, user_id))

@folder_bp.route('/<folder_name>/web_urls', methods=['PUT'])
def add_folder_web_urls(user_id, folder_name):
    data = request.json
    return jsonify(folder_service.add_web_urls(folder_name, data['web_urls'], user_id).to_dict())

@folder_bp.route('/<folder_name>/web_urls/<web_url>', methods=['DELETE'])
def delete_folder_web_urls(user_id, folder_name, web_url):
    return jsonify(folder_service.delete_web_urls(folder_name, web_url, user_id).to_dict())

# folder image_urls
@folder_bp.route('/<folder_name>/image_urls', methods=['GET'])
def get_folder_image_urls(user_id, folder_name):
    return jsonify(folder_service.get_image_urls(folder_name, user_id))

@folder_bp.route('/<folder_name>/image_urls', methods=['PUT'])
def add_folder_image_urls(user_id, folder_name):
    data = request.json
    return jsonify(folder_service.add_image_urls(folder_name, data['image_urls'], user_id).to_dict())

@folder_bp.route('/<folder_name>/image_urls/<image_url>', methods=['DELETE'])
def delete_folder_image_urls(user_id, folder_name, image_url):
    return jsonify(folder_service.delete_image_urls(folder_name, image_url, user_id).to_dict()) 


# folder download_urls
@folder_bp.route('/<folder_name>/download_urls', methods=['GET'])
def get_folder_download_urls(user_id, folder_name):
    return jsonify(folder_service.get_download_urls(folder_name, user_id))

@folder_bp.route('/<folder_name>/download_urls', methods=['PUT'])
def add_folder_download_urls(user_id, folder_name):
    data = request.json
    return jsonify(folder_service.add_download_urls(folder_name, data['download_urls'], user_id).to_dict())

@folder_bp.route('/<folder_name>/download_urls/<download_url>', methods=['DELETE'])
def delete_folder_download_urls(user_id, folder_name, download_url):
    return jsonify(folder_service.delete_download_urls(folder_name, download_url, user_id).to_dict()) 
