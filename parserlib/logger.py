import logging
from parserlib.paths import log_file


# Настройка логирования
formatter = logging.Formatter('[%(asctime)s] [%(filename)s:%(lineno)d %(threadName)s] [%(name)s] [%(levelname)s] - %(message)s')
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)

# Объект логера
logger = logging.getLogger("Dashboard Parser")      # Инициализируем объект логера
logger.handlers = [file_handler]                    # Устанавливаем единственный обработчик логера
logger.setLevel(logging.INFO)                       # Устанавливаем уровень логера