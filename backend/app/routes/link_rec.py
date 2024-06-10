from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import List

# from ..services.link_recommendation import get_links, insert_browsing_history
from ..models.rag_model import LinkRecInput, LinkList, VisitDataList

from flask import Blueprint, jsonify, request
from ..services.link_rec import LinkRec

link_rec_bp = Blueprint("link_rec_bp", __name__)
link_rec_service = LinkRec()

"""
takes in {"query" : str}
outputs {links_list: List[HttpUrl]}
"""


@link_rec_bp.route("/<user_id>", methods=["POST"])
def rec_links(user_id: str) -> LinkList:
    data = request.get_json()
    res = link_rec_service.get_links(user_id, data["query"])
    return jsonify(res), 201


"""
takes in {"my_list" : [visitdatas]}
outputs nothing
"""


@link_rec_bp.route("/insert_browsing_history", methods=["POST"])
def insert_history():
    data = request.get_json()
    link_rec_service.insert_browsing_history(data=data["my_list"])
    return jsonify({"message": "inserted successfully"})


# router = APIRouter()


# @router.post("/get_links/{user_id}", response_model=LinkList)
# def get_links_route(user_id: str, req_body: LinkRecInput = Body(...)):
#     try:
#         desc = req_body.query
#         return get_links(user_id, desc)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/insert_browsing_history", status_code=201)
# def insert_browsing_history_route(data: VisitDataList = Body(...)) -> None:
#     try:
#         insert_browsing_history(data.my_list)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
