from .intent_executor import IntentExecutor


class WebsearchIntentExecutor(IntentExecutor):
  def __init__(self, llm):
    self.llm = llm

  def support(self, intent):
    return intent.startswith("sample")

  def execute(self, intent):
    print(f"Executing intent: {intent}")
