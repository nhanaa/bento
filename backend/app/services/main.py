from fastapi import FastAPI, HTTPException, Body
from agent import create_agent
from pydantic import BaseModel


app = FastAPI()


class ChatInput(BaseModel):
    text: str


@app.post("/chat/{user_id}/{folder_id}")
def query_agent(user_id: str, folder_id: str, query: ChatInput = Body(...)):
    """
    [query] is the user's input in the request body
    data = {"text": prompt}
    """
    try:
        agent_with_chat_history = create_agent(user_id, folder_id)
        query_response = agent_with_chat_history.invoke(
            {"input": query.text, "folder_topic": "Economics"},
            config={"configurable": {"user_id": user_id, "folder_id": folder_id}},
        )
        return query_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
