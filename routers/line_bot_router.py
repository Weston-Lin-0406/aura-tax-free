import json
from fastapi import APIRouter, Request

from library.dao import LineChat, LineChatDao

router = APIRouter(
    prefix="/line-bot",
    tags=["line-bot"]
)

@router.post("/hook")
async def hook(request: Request):
    body = await request.body()
    chat_dict = json.loads(body)
    event = chat_dict["events"][0]
    message = event["message"]
    source = event["source"]
    if message["type"] == "text":
        chat = LineChat(source["userId"], message["text"])
        LineChatDao().create(chat)