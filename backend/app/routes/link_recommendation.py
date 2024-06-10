from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import List
from ..services.link_recommendation import get_links, insert_browsing_history
from ..models.rag_model import LinkRecInput, LinkList, VisitDataList

router = APIRouter()


@router.post("/get_links/{user_id}", response_model=LinkList)
def get_links_route(user_id: str, req_body: LinkRecInput = Body(...)):
    try:
        desc = req_body.query
        return get_links(user_id, desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert_browsing_history", status_code=201)
def insert_browsing_history_route(data: VisitDataList = Body(...)) -> None:
    try:
        insert_browsing_history(data.my_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
