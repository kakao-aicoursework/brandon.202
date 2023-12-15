from utils.localfile_loader import read_file
from .websearch import search
from .intent_executor import IntentExecutor
from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate


class WebsearchIntentExecutor(IntentExecutor):
  def __init__(self, llm):
    self.step1 = LLMChain(
      llm=llm,
      prompt=ChatPromptTemplate.from_template(
        template=read_file("./infrastructure/model/templates/websearch_parse_keyword_template.txt"),
      ),
      output_key="output",
      verbose=True,
    )
    self.step2 = LLMChain(
      llm=llm,
      prompt=ChatPromptTemplate.from_template(
        template=read_file("./infrastructure/model/templates/websearch_response_template.txt"),
      ),
      output_key="output",
      verbose=True,
    )

  def support(self, intent):
    return intent == "websearch"

  def execute(self, context):
    keyword = self.step1.run(context)
    context["websearch_keyword"] = keyword
    context["websearch_result"] = search(keyword)
    return self.step2.run(context)
