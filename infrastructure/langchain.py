from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate

# load .env
load_dotenv()

# ChatGPT
llm = ChatOpenAI(
  temperature=0,
  max_tokens=3000,
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
      create_template_chain("./infrastructure/templates/retrieve_template.txt", "response"),
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
