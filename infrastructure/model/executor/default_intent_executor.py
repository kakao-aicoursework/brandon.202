from .intent_executor import IntentExecutor


class FailbackIntentExecutor(IntentExecutor):
  def __init__(self, llm):
    self.llm = llm

  def support(self, intent):
    return True

  def execute(self, intent):
    print(f"Executing intent: {intent}")
