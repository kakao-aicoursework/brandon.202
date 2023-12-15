def read_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    total_text = file.read()
  return total_text