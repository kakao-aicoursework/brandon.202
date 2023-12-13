import aiohttp

from presentations.dto.chatbot_request import ChatbotRequest


async def send_simple_text(request: ChatbotRequest, message) -> dict:
  # 참고링크 통해 payload 구조 확인 가능
  # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
  # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format
  payload = {
    "version": "2.0",
    "template": {
      "outputs": [
        {
          "simpleText": {
            "text": message
          }
        }
      ]
    }
  }
  url = request.userRequest.callbackUrl
  if url:
    async with aiohttp.ClientSession() as session:
      async with session.post(url=url, json=payload, ssl=False) as resp:
        await resp.json()
