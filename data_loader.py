import glob

import chromadb


def read_txt_files_in_directory(directory_path='./data/'):
  txt_files = glob.glob(f'{directory_path}/*.txt')
  files = []
  for txt_file in txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
      content = file.read()
      files.append({
        'name': file.name,
        'content': content
      })
  return files


def initialize_data():
  client = chromadb.PersistentClient()
  kakao_data_collection = client.get_or_create_collection(
    name="kakao-data",
    metadata={"hnsw:space": "cosine"}
  )
  files = read_txt_files_in_directory('./data/')
  for idx, file in enumerate(files, start=1):
    kakao_data_collection.add(
      documents=file.content,
      metadatas=file.name,
      ids=idx
    )
