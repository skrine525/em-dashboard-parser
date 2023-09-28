import json, os
from parserlib import paths


# Открываем json-файл конфига
if not os.path.exists(paths.config_file):
    raise FileNotFoundError("File 'config.json' does not exists")

# Парсим данные внутри config.json
config_file = open(paths.config_file, encoding='utf-8')
config_data = json.loads(config_file.read())
config_file.close()

# Достаем значения из словаря и заносим в константы
SQL_HOST = config_data['SQL_HOST']
SQL_USERNAME = config_data['SQL_USERNAME']
SQL_PASSWORD = config_data['SQL_PASSWORD']
SQL_DATABASE = config_data['SQL_DATABASE']
ARGUS_USERNAME = config_data['ARGUS_USERNAME']
ARGUS_PASSWORD = config_data['ARGUS_PASSWORD']
EMAIL_SERVER =  config_data['EMAIL_SERVER']
EMAIL_ADDRESS = config_data['EMAIL_ADDRESS']
EMAIL_PASSWORD = config_data['EMAIL_PASSWORD']

# Меняем значение files_dir, если указанная в конфиг файле директория существует
if os.path.exists(config_data['FILES_DIR']):
    paths.files_dir = config_data['FILES_DIR']
    paths.create_dirs()

# Очищаем ненужные переменные
del config_file
del config_data
