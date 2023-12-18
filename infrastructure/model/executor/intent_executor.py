from abc import ABC, abstractmethod


class IntentExecutor(ABC):
  @abstractmethod
  def support(self, intent):
    pass
  
  @abstractmethod
  def execute(self, context):
    pass
