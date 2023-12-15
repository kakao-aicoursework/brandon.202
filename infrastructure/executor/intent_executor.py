from abc import ABC, abstractmethod


class IntentExecutor(ABC):
  @abstractmethod
  def execute(self, intent):
    pass

  @abstractmethod
  def support(self, intent):
    pass
