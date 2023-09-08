import json, os


# Путь к конфиг файлу
CONFIG_PATH  = "config.json"

# Открываем json-файл конфига
if not os.path.exists("config.json"):
    raise FileNotFoundError("File 'config.json' does not exists")

# Парсим данные внутри config.json
config_file = open(CONFIG_PATH, encoding='utf-8')
config_data = json.loads(config_file.read())
config_file.close()

# Достаем значения из словаря и заносим в константы
FILES_DIR = config_data['FILES_DIR']
SQL_HOST = config_data['SQL_HOST']
SQL_USERNAME = config_data['SQL_USERNAME']
SQL_PASSWORD = config_data['SQL_PASSWORD']
SQL_DATABASE = config_data['SQL_DATABASE']
ARGUS_USERNAME = config_data['ARGUS_USERNAME']
ARGUS_PASSWORD = config_data['ARGUS_PASSWORD']
EMAIL_SERVER =  config_data['EMAIL_SERVER']
EMAIL_ADDRESS = config_data['EMAIL_ADDRESS']
EMAIL_PASSWORD = config_data['EMAIL_PASSWORD']

# Очищаем ненужные переменные
del config_file
del config_data
