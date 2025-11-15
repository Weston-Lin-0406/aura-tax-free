import json
from fastapi import APIRouter, Request
from pyfk import get_logger

from library.dao import LineChat, LineChatDao

router = APIRouter(
    prefix="/line-bot",
    tags=["line-bot"]
)

log = get_logger()

@router.post("/hook")
async def hook(request: Request):
    body = await request.body()
    chat_dict = json.loads(body)
    log.info(chat_dict)
    event = chat_dict["events"][0]
    message = event["message"]
    source = event["source"]
    if message["type"] == "text":
        chat = LineChat(source["userId"], message["text"])
        LineChatDao().create(chat)