import logging


# Настройка логирования
formatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d %(threadName)s] [%(name)s] [%(levelname)s] - %(message)s')
file_handler = logging.FileHandler("parser.log", encoding='utf-8')
file_handler.setFormatter(formatter)
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler]
)

# Объект логера
logger = logging.getLogger("Parser")