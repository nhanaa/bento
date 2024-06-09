from pydantic import BaseModel, HttpUrl, Field
from typing import List
from datetime import datetime


class LinkRecInput(BaseModel):
    query: str


class LinkList(BaseModel):
    links_list: List[HttpUrl]


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
