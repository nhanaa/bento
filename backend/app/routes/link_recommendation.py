from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel
from typing import List
from ..services.link_recommendation import get_links
from ..models.rag_pipeline import LinkRecInput, LinkList

router = APIRouter()


@router.post("/get_links/{user_id}", response_model=LinkList)
def get_links_route(user_id: str, req_body: LinkRecInput = Body(...)):
    try:
        print("before: ", req_body)
        desc = req_body.query
        print("after: ", desc)
        return get_links(user_id, desc)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
