from fastapi import FastAPI, APIRouter, Body, HTTPException
from ..services.chat import query_agent
from ..models.rag_model import ChatInput, ChatOutput

router = APIRouter()


@router.post("/chat/{user_id}/{folder_id}", response_model=ChatOutput)
async def query_agent_route(user_id: str, folder_id: str, query: ChatInput = Body(...)):
    try:
        print(query)
        res = await query_agent(user_id, folder_id, query.text)
        # print("my response is", res)
        return {"output": res["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
