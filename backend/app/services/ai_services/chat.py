from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from agent import create_agent


async def query_agent(user_id: str, folder_id: str, query: str):
    """
    [query] is the user's input in the request body
    data = {"text": prompt}
    """
    agent_with_chat_history = create_agent(user_id, folder_id)
    query_response = agent_with_chat_history.invoke(
        {"input": query, "folder_topic": "machine learning/AI/NLP"},
        config={"configurable": {"user_id": user_id, "folder_id": folder_id}},
    )
    return query_response
