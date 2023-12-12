import time
import aiohttp
import glob
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains import LLMChain

from dto import ChatbotRequest

# load .env
load_dotenv()
message_template = f"""
**(중요) 20자 내외로만 대답해**

너는 법인 "카카오" 서비스의 Chatbot이야. 너의 고객은 한국인이며 그러니까 한국어로 대화해주길 바래.
가능한 친절하게 답변을 하고 상대방이 이해할 수 있도록 단계적으로 대답해주길 원해

요청은 이거야
'''
{{user_message}}
```
"""

# ChatGPT
llm = ChatOpenAI(
  temperature=0,
  max_tokens=300,
  model="gpt-3.5-turbo-16k")

def read_template_text(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    total_text = file.read()
  return total_text

def create_template_chain(template_path, output_key):
  return LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
      template=read_template_text(template_path),
    ),
    output_key=output_key,
    verbose=True,
  )

def generate_message(user_message) -> dict[str, str]:
  preprocess_chain = SequentialChain(
    chains=[
      create_template_chain("./templates/retrieve_template.txt", "response"),
    ],
    input_variables=["user_message"],
    output_variables=["response"],
    verbose=True,
  )

  context = preprocess_chain(dict(
    user_message=user_message
  ))
  print(context)
  return context["response"]

async def callback_handler(request: ChatbotRequest) -> dict:
  response = generate_message(request.userRequest.utterance)
  print(response)
  output_text = response

  # 참고링크 통해 payload 구조 확인 가능
  payload = {
    "version": "2.0",
    "template": {
      "outputs": [
        {
          "simpleText": {
            "text": output_text
          }
        }
      ]
    }
  }
  # ===================== end =================================
  # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/ai_chatbot_callback_guide
  # 참고링크1 : https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

  time.sleep(1.0)
  url = request.userRequest.callbackUrl

  if url:
    async with aiohttp.ClientSession() as session:
      async with session.post(url=url, json=payload, ssl=False) as resp:
        await resp.json()
