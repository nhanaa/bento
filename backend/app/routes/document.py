from flask import Blueprint, jsonify, request
from services.ai_services.document import Document

document_bp = Blueprint("document_bp", __name__)
document_service = Document()

"""
input= {links_list: [urls]}
output= success str
"""


@document_bp.route("/<user_id>/<folder_id>", methods=["POST"])
async def process_documents(user_id, folder_id):
    data = request.get_json()
    links_list = data["links_list"]
    await document_service.process_many_documents(user_id, folder_id, links_list)
    return {"message": "created document and chunks successfully"}
