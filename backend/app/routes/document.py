from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Body
from typing import Any, List
from pydantic import BaseModel, HttpUrl, Field

from ..services.document import process_one_document
from ..models.rag_model import LinkList
from asyncio import gather


router = APIRouter()


@router.post("/process_documents/{user_id}/{folder_id}")
async def process_documents(
    user_id: str, folder_id: str, req_body: LinkList = Body(...)
) -> Any:
    try:
        links_list = req_body.links_list
        # for link in links_list:
        #     await process_one_document(
        #         user_id=user_id, folder_id=folder_id, url=str(link)
        #     )
        tasks = [
            process_one_document(user_id=user_id, folder_id=folder_id, url=str(link))
            for link in req_body.links_list
        ]
        await gather(*tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def get():
    return {"test": "here is the example text"}
