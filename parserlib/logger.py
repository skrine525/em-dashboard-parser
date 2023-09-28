import logging
from parserlib.paths import log_file


# Настройка логирования
formatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d %(threadName)s] [%(name)s] [%(levelname)s] - %(message)s')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler]
)

# Объект логера
logger = logging.getLogger("Dashboard Parser")