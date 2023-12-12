import json
import os

import openai
from dotenv import load_dotenv

from vectordb import find_kakao_data

# load .env
load_dotenv()
openai.api_key = os.environ["API_KEY"]


def get_initial_messages():
  return [
    {
      "role": "system",
      "content": '''
            너는 법인 "카카오" 서비스의 Chatbot이야. 너의 고객은 한국인이며 그러니까 한국어로 대화해주길 바래.
            가능한 친절하게 답변을 하고 상대방이 이해할 수 있도록 단계적으로 대답해주길 원해
            '''
    }
  ]


def get_functions():
  return [
    {
      "name": "find_kakao_data",
      "description": "카카오 관련 된 정보를 찾아올 수 있습니다",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "카카오 관련 정보중 궁금한 내용",
          },
        },
        "required": ["playlist_csv"],
      },
    }
  ]


def send_message(
    messages,
    gpt_model="gpt-3.5-turbo",
    temperature=0.1):
  response = openai.ChatCompletion.create(
    model=gpt_model,
    messages=messages,
    temperature=temperature,
    functions=get_functions(),
    function_call='auto',
  )
  response_message = response["choices"][0]["message"]

  if response_message.get("function_call"):
    available_functions = {
      "find_kakao_data": find_kakao_data,
    }
    function_name = response_message["function_call"]["name"]
    fuction_to_call = available_functions[function_name]
    function_args = json.loads(response_message["function_call"]["arguments"])
    function_response = fuction_to_call(**function_args)
    messages.append(response_message)
    messages.append(
      {
        "role": "function",
        "name": function_name,
        "content": json.dumps(function_response, ensure_ascii=False),
      }
    )
    print("----")
    print(messages)

    response = openai.ChatCompletion.create(
      model=gpt_model,
      messages=messages,
      temperature=temperature,
    )
  return response.choices[0].message.content
