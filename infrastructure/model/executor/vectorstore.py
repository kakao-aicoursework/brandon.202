import os

from dotenv import load_dotenv
from langchain.document_loaders import (
  TextLoader,
)
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

# load .env
load_dotenv()

CHROMA_COLLECTION_NAME = "kakao-bot"
CHROMA_PERSIST_PATH = "./persistence/kakao-chroma"

def upload_embedding_from_file(file_path):
  loader = {
    "txt": TextLoader,
  }.get(file_path.split(".")[-1])
  if loader is None:
    raise ValueError("Not supported file type")
  documents = loader(file_path).load()
  text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
  docs = text_splitter.split_documents(documents)
  print(docs, end='\n\n\n')

  Chroma.from_documents(
    docs,
    OpenAIEmbeddings(),
    collection_name=CHROMA_COLLECTION_NAME,
    persist_directory=CHROMA_PERSIST_PATH,
  )
  print('db success')


def upload_embeddings_from_dir(dir_path):
  failed_upload_files = []
  for root, dirs, files in os.walk(dir_path):
    for file in files:
      if file.endswith(".txt"):
        file_path = os.path.join(root, file)

        try:
          upload_embedding_from_file(file_path)
          print("SUCCESS: ", file_path)
        except Exception as e:
          print("FAILED: ", file_path + f"by({e})")
          failed_upload_files.append(file_path)


# upload_embeddings_from_dir("./infrastructure/data")
db = Chroma(
  persist_directory=CHROMA_PERSIST_PATH,
  collection_name=CHROMA_COLLECTION_NAME,
  embedding_function=OpenAIEmbeddings(),
)
retriever = db.as_retriever()

def query_on_chroma(query: str, use_retriever: bool = False) -> list[str]:
  if use_retriever:
    docs = retriever.get_relevant_documents(query)
  else:
    docs = db.similarity_search(query)
  str_docs = [doc.page_content for doc in docs]
  return str_docs
