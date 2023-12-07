import glob

from vectordb import kakao_collection


# '#'을 기준으로 제목과 컨텐트를 뽑아옴
def parse_data(input_str):
  data_list = []
  sections = input_str.split('\n#')[1:]
  for section in sections:
    title, content = map(str.strip, section.split('\n', 1))
    data_list.append({'title': title, 'content': content})
  return data_list


def read_txt_files_in_directory(directory_path='./data/'):
  txt_files = glob.glob(f'{directory_path}/*.txt')
  id_count = 1
  ids = []
  metadatas = []
  documents = []
  for txt_file in txt_files:
    with open(txt_file, 'r', encoding='utf-8') as file:
      total_text = file.read()
      parsed_data = parse_data(total_text)
      for parsed_element in parsed_data:
        ids.append("id" + str(id_count))
        documents.append(
          "title: " + parsed_element['title'] + "\n"
                                                "content: " + parsed_element[
            'content'])
        metadatas.append({'name': file.name,
                          'title': parsed_element['title'],
                          'content': parsed_element['content']})
        id_count += 1
  return ids, metadatas, documents


def initialize_data():
  ids, metadatas, documents = read_txt_files_in_directory('./data/')
  kakao_collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
  )
