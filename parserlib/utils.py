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
    if directory == os.path.basename(paths.cci_dir):
        dst = paths.archive_cci_dir
    elif directory == os.path.basename(paths.freight_dir):
        dst = paths.archive_freight_dir
    elif directory == os.path.basename(paths.ici3_dir):
        dst = paths.archive_ici3_dir
    elif directory == os.path.basename(paths.vostochny_dir):
        dst = paths.archive_vostochny_dir
    elif directory == os.path.basename(paths.manual_dir):
        dst = paths.archive_manual_dir
    elif directory == os.path.basename(paths.rail_export_dir):
        dst = paths.archive_rail_export_dir
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
    