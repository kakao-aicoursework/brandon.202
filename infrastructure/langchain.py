from infrastructure.model import AutonomousAgent


def generate_message(user_message, conversation_id: str = "dummy") -> dict[str, str]:
  model = AutonomousAgent(conversation_id)
  return model.run(user_message, conversation_id)
