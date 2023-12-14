from langchain.utilities import DuckDuckGoSearchAPIWrapper

duckduckgo = DuckDuckGoSearchAPIWrapper(region='kr-kr')


def truncate_text(text, max_length=3000):
  if len(text) > max_length:
    truncated_text = text[:max_length - 3] + '...'
  else:
    truncated_text = text
  return truncated_text


def search(message):
  return truncate_text(duckduckgo.run(message))