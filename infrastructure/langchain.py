from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from infrastructure.vectorstore import query_on_chroma

# load .env
load_dotenv()


def read_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    total_text = file.read()
  return total_text


def create_template_chain(llm, template_path, output_key):
  return LLMChain(
    llm=llm,
    prompt=ChatPromptTemplate.from_template(
      template=read_file(template_path),
    ),
    output_key=output_key,
    verbose=True,
  )


def create_chains():
  llm = ChatOpenAI(
    temperature=0,
    max_tokens=3000,
    model="gpt-3.5-turbo-16k")
  return {
    'guess_intent': create_template_chain(
      llm=llm,
      template_path="./infrastructure/templates/guess_intent.txt",
      output_key="intent",
    ),
    'retrieve_kakao_data': create_template_chain(
      llm=llm,
      template_path="./infrastructure/templates/retrieve_template.txt",
      output_key="output",
    ),
    'default': create_template_chain(
      llm=llm,
      template_path="./infrastructure/templates/default_response_template.txt",
      output_key="output",
    )
  }


def generate_message(user_message) -> dict[str, str]:
  chains = create_chains()
  context = dict(user_message=user_message)
  context["input"] = context["user_message"]
  context["intent_list"] = read_file(
    "./infrastructure/templates/intent_list.txt")
  intent = chains["guess_intent"].run(context)

  print(intent)
  if intent == "retrieve_kakao_data":
    context["retrieve_result"] = query_on_chroma(context["user_message"])
    result = chains["retrieve_kakao_data"].run(context)
  else:
    result = chains["default"].run(context["user_message"])
  print(result)
  return result
