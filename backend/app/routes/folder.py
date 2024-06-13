from flask import Blueprint, request, jsonify
from services.folder import FolderService

folder_bp = Blueprint('folders', __name__)
folder_service = FolderService()

# folders
@folder_bp.route('/<user_id>', methods=['POST'])
def add_folder(user_id):
    data = request.json
    folder = folder_service.create_folder(data['folder_name'], data['summary'], user_id)
    return jsonify(folder), 201

@folder_bp.route('/<user_id>/all', methods=['GET'])
def get_folders_by_user_id(user_id):
    return jsonify(folder_service.get_folders_by_user_id(user_id))

@folder_bp.route('/<user_id>', methods=['GET'])
def get_folder(user_id):
    data = request.json
    return jsonify(folder_service.get_folder_by_name(data['folder_name'], user_id))


# folder web_urls
@folder_bp.route('/<user_id>/web_urls', methods=['GET'])
def get_folder_web_urls(user_id):
    data = request.json
    return jsonify(folder_service.get_web_urls(data['folder_name'], user_id))

@folder_bp.route('/<user_id>/web_urls/add', methods=['PUT'])
def add_folder_web_urls(user_id):
    data = request.json
    return jsonify(folder_service.add_web_urls(data['folder_name'], data['web_urls'], user_id))

@folder_bp.route('/<user_id>/web_urls/delete', methods=['PUT'])
def delete_folder_web_urls(user_id):
    data = request.json
    return jsonify(folder_service.delete_web_urls(data['folder_name'], data['web_urls'], user_id)) 


# folder image_urls
@folder_bp.route('/<user_id>/image_urls', methods=['GET'])
def get_folder_image_urls(user_id):
    data = request.json
    return jsonify(folder_service.get_image_urls(data['folder_name'], user_id))

@folder_bp.route('/<user_id>/image_urls/add', methods=['PUT'])
def add_folder_image_urls(user_id):
    data = request.json
    return jsonify(folder_service.add_image_urls(data['folder_name'], data['image_urls'], user_id))

@folder_bp.route('/<user_id>/image_urls/delete', methods=['PUT'])
def delete_folder_image_urls(user_id):
    data = request.json
    return jsonify(folder_service.delete_image_urls(data['folder_name'], data['image_urls'], user_id)) 


# folder download_urls
@folder_bp.route('/<user_id>/download_urls', methods=['GET'])
def get_folder_download_urls(user_id):
    data = request.json
    return jsonify(folder_service.get_download_urls(data['folder_name'], user_id))

@folder_bp.route('/<user_id>/download_urls/add', methods=['PUT'])
def add_folder_download_urls(user_id, folder_name):
    data = request.json
    return jsonify(folder_service.add_download_urls(data['folder_name'], data['download_urls'], user_id))

@folder_bp.route('/<user_id>/download_urls/delete', methods=['PUT'])
def delete_folder_download_urls(user_id, folder_name):
    data = request.json
    return jsonify(folder_service.delete_download_urls(data['folder_name'], data['download_urls'], user_id)) 
