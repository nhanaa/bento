from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import List

# from ..services.link_recommendation import get_links, insert_browsing_history
from models.rag_model import LinkRecInput, LinkList, VisitDataList

from flask import Blueprint, jsonify, request
from services.ai_services.link_rec import LinkRec

link_rec_bp = Blueprint("link_rec_bp", __name__)
link_rec_service = LinkRec()

"""
takes in {"query" : str}
outputs {links_list: List[HttpUrl]}
"""

@link_rec_bp.route("/<ip>", methods=["POST"])
def rec_links(ip: str) -> LinkList:
    data = request.get_json()
    res = link_rec_service.get_links(ip, data["query"])
    return jsonify(res), 201
