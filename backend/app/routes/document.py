from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Body
from typing import Any, List
from pydantic import BaseModel, HttpUrl, Field

from ..models.rag_model import LinkList
from asyncio import gather


from flask import Blueprint, jsonify, request

from ..services.document import Document

document_bp = Blueprint("document_bp", __name__)
document_service = Document()

"""
input= {links_list: [urls]}
output= success str
"""


@document_bp.route("/<user_id>/<folder_id>", methods=["POST"])
async def process_documents(user_id, folder_id):
    data = request.get_json()
    await document_service.process_many_documents(
        user_id, folder_id, data["links_list"]
    )
    return {"message": "created document and chunks successfully"}
