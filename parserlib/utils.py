import os
from parserlib import paths
from parserlib.logger import logger


# Исключение: Неизвестная директория
class UnknownDirectoryError(Exception):
    def __init__(self, directory):
        self.directory = directory
        super().__init__(f"Unknown directory: {directory}")

# Помещает файл в архив
def archive_file(src: str):
    # Проверяем существование файла
    if not os.path.exists(src):
        raise FileNotFoundError(f"Incorrect path: {src}")
    
    # Получаем название файла и путь к папке, в которой лежит файл
    filename = os.path.basename(src)
    directory = os.path.basename(os.path.dirname(src))
    dst = ""                                                            # Место назначения файла
    
    # Определяем, куда класть файл
    if directory == os.path.basename(paths.CCI_DIR):
        dst = paths.ARCHIVE_CCI_DIR
    elif directory == os.path.basename(paths.FREIGHT_DIR):
        dst = paths.ARCHIVE_FREIGHT_DIR
    elif directory == os.path.basename(paths.ICI3_DIR):
        dst = paths.ARCHIVE_ICI3_DIR
    elif directory == os.path.basename(paths.VOSTOCHNY_DIR):
        dst = paths.ARCHIVE_VOSTOCHNY_DIR
    else:
        raise UnknownDirectoryError(directory)
    
    # Формируем путь назначения
    dst = os.path.join(dst, filename)
    
    # Выполянем перенос файла
    if os.path.exists(dst):
        # Если файл уже в архиве - удаляем файл
        os.remove(src)
        logger.info(f"File is already archived: {src}")
    else:
        # Если файл не в архиве - переносим в архив
        os.rename(src, dst)
        logger.info(f"File archived: {src}")
    