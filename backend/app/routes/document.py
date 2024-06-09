from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Body
from typing import Any, List
from pydantic import BaseModel, HttpUrl, Field

from ..services.document import process_one_document
from datetime import datetime


router = APIRouter()


class Document(BaseModel):
    title: str = Field(
        ..., title="Document Title", description="The title of the document"
    )
    summary: str = Field(
        ..., title="Summary", description="A brief summary of the document"
    )
    created_date: datetime = Field(
        default_factory=datetime.now,
        title="Creation Date",
        description="The date and time the document was created",
    )

    # chunk_ids: List[str]


class ProcessDocInput(BaseModel):
    links_list: List[HttpUrl]


@router.post("/process_documents/{user_id}/{folder_id}")
def process_documents(
    user_id: str, folder_id: str, req_body: ProcessDocInput = Body(...)
) -> Any:
    try:
        links_list = req_body.links_list
        for link in links_list:
            process_one_document(user_id=user_id, folder_id=folder_id, url=str(link))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
def get():
    return {"test": "here is the example text"}
