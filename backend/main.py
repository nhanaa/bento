import requests
from fastapi import FastAPI
from app.routes import document, summary, chat
from fastapi.middleware.cors import CORSMiddleware

from backend.app.routes import link_rec

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(document.router)
app.include_router(link_rec.router)
app.include_router(summary.router)
app.include_router(chat.router)
