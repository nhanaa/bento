import requests
from fastapi import FastAPI
from app.routes import document, link_recommendation, summary
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(link_recommendation.router)
app.include_router(summary.router)
