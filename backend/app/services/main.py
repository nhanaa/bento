from fastapi import FastAPI
from agent import agent_with_chat_history

app = FastAPI()


@app.post("/chat/{user_id}/{folder_id}")
def query_agent(query, user_id: str, folder_id: str):
    """
    [query] is the user's input in the request body
    data = {"text": prompt}
    """
    query_response = agent_with_chat_history.invoke(
        {"input": query.text, "folder_topic": "Machine Learning/AI"},
        config={"configurable": {"user_id": user_id, "folder_id": folder_id}},
    )
    return query_response
