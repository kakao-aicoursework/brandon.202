from .intent_executor import IntentExecutor


class RetrieveKakaoDataIntentExecutor(IntentExecutor):
  def __init__(self, llm):
    self.llm = llm

  def support(self, intent):
    return intent.startswith("retrieve_kakao_data")

  def execute(self, intent):
    print(f"Executing intent: {intent}")
