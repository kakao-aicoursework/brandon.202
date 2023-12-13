import infrastructure

from presentations.dto.chatbot_request import ChatbotRequest


async def answer(request: ChatbotRequest) -> dict:
  response = infrastructure.generate_message(request.userRequest.utterance)
  await infrastructure.send_simple_text(request, response)
