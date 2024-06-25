from services.ai_services.chat import query_agent
from flask import Blueprint, jsonify, request

chat_bp = Blueprint("chat_bp", __name__)

"""
takes in {"query" : str}
outputs {"output" : AI message in term of str}
"""


@chat_bp.route("/<user_id>/<folder_id>", methods=["POST"])
async def query_agent_route(user_id: str, folder_id: str):
    data = request.get_json()
    res = await query_agent(user_id, folder_id, data["query"])
    # print("my response is", res)
    return {"output": res["output"]}
