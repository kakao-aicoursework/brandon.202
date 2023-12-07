import ai_model
import gui
import vectordb_initializer


def main():
  vectordb_initializer.initialize_data()
  messages = ai_model.get_initial_messages()
  gui.initialize(messages)


if __name__ == "__main__":
  main()
