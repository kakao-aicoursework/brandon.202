from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from .history_storage import load_conversation_history, get_chat_history, log_qna
from infrastructure.model.executor import RetrieveKakaoDataIntentExecutor, WebsearchIntentExecutor, FailbackIntentExecutor
from utils.localfile_loader import read_file

# load .env
load_dotenv()

class AutonomousAgent():
  def __init__(self, max_loop: int = 5):
    llm = ChatOpenAI(
      temperature=0,
      max_tokens=3000,
      model="gpt-3.5-turbo-16k")
    self.max_loop = max_loop
    self.guess_intent_chain = LLMChain(
      llm=llm,
      prompt=ChatPromptTemplate.from_template(
        template=read_file("./infrastructure/templates/guess_intent_template.txt"),
      ),
      output_key="intent",
      verbose=True,
    )
    self.executors = [
      RetrieveKakaoDataIntentExecutor(llm),
      WebsearchIntentExecutor(llm),
      FailbackIntentExecutor(llm),
    ]

  def run(self, user_message, conversation_id: str = "dummy"):
    history_file = load_conversation_history(conversation_id)
    context = dict(user_message=user_message)
    context["input"] = context["user_message"]
    context["intent_list"] = read_file("./infrastructure/templates/intent_list.txt")
    context["chat_history"] = get_chat_history(conversation_id)
    intent_loop_count = 0
    while self.count < self.max_count:
      intent = self.guess_intent_chain(context)
      for executor in self.executors:
        if(executor.support(intent)):
          answer = executor.run(intent, context)
      intent_loop_count += 1
      print(f"[INTENT]: {intent}, [LOOP] ({intent_loop_count} / {self.max_loop})")
    log_qna(history_file, user_message, answer)
