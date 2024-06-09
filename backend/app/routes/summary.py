from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, HttpUrl
from typing import Any
from fastapi import APIRouter
import os
import sys

print(sys.path)
# from backend.app.services.summarization import summarize_pdf
from ..services.summarization import summarize_pdf
router = APIRouter()


class SummarizeOutput(BaseModel):
    summary: str
    title: str


class SummarizeInput(BaseModel):
    url: HttpUrl


@router.post("/summarize/", response_model=SummarizeOutput)
def summarize(req_body: SummarizeInput = Body(...)) -> Any:
    try:
        result = summarize_pdf(str(req_body.url))
        print(result)
        return SummarizeOutput(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
