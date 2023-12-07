import chromadb

vectordb_client = chromadb.PersistentClient()
kakao_collection = vectordb_client.get_or_create_collection(
  name="kakao-data",
  metadata={"hnsw:space": "cosine"}
)


def find_kakao_data(query):
  return kakao_collection.query(
    query_texts=[query],
    n_results=5,
  )
