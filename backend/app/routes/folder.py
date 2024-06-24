from flask import Blueprint, request, jsonify
from langchain_core.output_parsers import StrOutputParser
from ..services.folder import FolderService
from ..services.ai_services.prompt import folder_prompt
from ..utils.ai_tools import llm


folder_bp = Blueprint("folders", __name__)
folder_service = FolderService()


# folders
@folder_bp.route("/", methods=["POST"])
def add_folder():
    data = request.get_json()
    folder = folder_service.create_folder(
        data["user_id"], data["name"], data["summary"]
    )
    return jsonify(folder), 201


@folder_bp.route("/all/<user_id>", methods=["GET"])
def get_folders_by_user_id(user_id):
    folders = folder_service.get_folders_by_user_id(user_id)
    if not folders:
        return jsonify({"error": "Folders not found"}), 404
    return jsonify(folders)


@folder_bp.route("/<folder_id>/", methods=["GET"])
def get_folder(folder_id):
    folder = folder_service.get_folder_by_id(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


@folder_bp.route("/<folder_id>/", methods=["PUT"])
def update_folder(folder_id):
    data = request.json
    folder = folder_service.update_folder_by_id(folder_id, data)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


@folder_bp.route("/<folder_id>/", methods=["DELETE"])
def delete_folder(folder_id):
    folder = folder_service.delete_folder_by_id(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify({"message": "Folder deleted successfully"})


# folder web_urls
@folder_bp.route("/<folder_id>/web_urls", methods=["GET"])
def get_folder_web_urls(folder_id):
    web_urls = folder_service.get_web_urls(folder_id)
    if web_urls == None:
        return jsonify({"error": "Web URLs not found"}), 404
    return jsonify(web_urls)


@folder_bp.route("/<folder_id>/web_urls", methods=["PUT"])
def add_folder_web_urls(folder_id):
    data = request.json
    folder = folder_service.add_web_urls(folder_id, data["web_urls"])
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


@folder_bp.route("/<folder_id>/web_urls", methods=["DELETE"])
def delete_folder_web_urls(folder_id):
    folder = folder_service.delete_web_urls(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


# folder image_urls
@folder_bp.route("/<folder_id>/image_urls", methods=["GET"])
def get_folder_image_urls(folder_id):
    image_urls = folder_service.get_image_urls(folder_id)
    if image_urls == None:
        return jsonify({"error": "Image URLs not found"}), 404
    return jsonify(image_urls)


@folder_bp.route("/<folder_id>/image_urls", methods=["PUT"])
def add_folder_image_urls(folder_id):
    data = request.json
    folder = folder_service.add_image_urls(folder_id, data["image_urls"])
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


@folder_bp.route("/<folder_id>/image_urls", methods=["DELETE"])
def delete_folder_image_urls(folder_id):
    folder = folder_service.delete_image_urls(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


# folder download_urls
@folder_bp.route("/<folder_id>/download_urls", methods=["GET"])
def get_folder_download_urls(folder_id):
    download_urls = folder_service.get_download_urls(folder_id)
    if download_urls == None:
        return jsonify({"error": "Download URLs not found"}), 404
    return jsonify(download_urls)


@folder_bp.route("/<folder_id>/download_urls", methods=["PUT"])
def add_folder_download_urls(folder_id):
    data = request.json
    folder = folder_service.add_download_urls(folder_id, data["download_urls"])
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


@folder_bp.route("/<folder_id>/download_urls", methods=["DELETE"])
def delete_folder_download_urls(folder_id):
    folder = folder_service.delete_download_urls(folder_id)
    if not folder:
        return jsonify({"error": "Folder not found"}), 404
    return jsonify(folder)


"""
in req body: {"query": folder description given by the user}
"""


@folder_bp.route("/get_summary/<folder_id>", methods=["POST"])
def get_folder_summary(folder_id):
    data = request.json
    list_of_summaries = folder_service.get_summary(folder_id)
    print(f"length of documents: {len(list_of_summaries)}")
    llm_chain = folder_prompt | llm | StrOutputParser()
    res = llm_chain.invoke({"summaries": list_of_summaries, "theme": data["query"]})
    return {"folder_summary": res}
