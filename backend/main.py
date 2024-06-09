import requests
from fastapi import FastAPI
from app.routes import document

app = FastAPI()

app.include_router(document.router)
