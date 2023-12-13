from fastapi import BackgroundTasks, APIRouter

from business.chatbot_service import answer
from .dto.chatbot_request import ChatbotRequest

root_router = APIRouter()

@root_router.get("/ping")
async def ping():
  return {
    "message": "pong"
  }


@root_router.post("/callback")
async def skill(req: ChatbotRequest, background_tasks: BackgroundTasks):
  background_tasks.add_task(answer, req)
  out = {
    "version": "2.0",
    "useCallback": True,
    "data": {
      "text": "생각하고 있는 중이에요😘 \n15초 정도 소요될 거 같아요 기다려 주실래요?!"
    }
  }
  return out
