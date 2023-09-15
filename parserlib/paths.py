import os, sys
from parserlib import config


# Константы
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # Путь к корневой папке приложения
DOWNLOADING_DIR = os.path.join(ROOT_DIR, "downloads")                           # Путь к папке с загруженными файлами
FILES_DIR = config.FILES_DIR                                                    # Путь к корневой папке парсинга
ARCHIVE_DIR = os.path.join(FILES_DIR, 'archive')                                # Путь к папке архивных файлов
CCI_DIR = os.path.join(FILES_DIR, "pdf_cci")                                    # Путь к папке с файлами CCI
FREIGHT_DIR = os.path.join(FILES_DIR, "pdf_freight")                            # Путь к папке с файлами Фрахьа
VOSTOCHNY_DIR = os.path.join(FILES_DIR, "xls_fob_vostochny")                    # Путь к папке с файлами FOB Vostochny
ICI3_DIR = os.path.join(FILES_DIR, "xls_ici3")                                  # Путь к папке с файлами ICI3
MANUAL_DIR = os.path.join(FILES_DIR, 'xlsx_manual')                             # Путь к папке с файлами Ручной XLSX
ARCHIVE_CCI_DIR = os.path.join(ARCHIVE_DIR, "pdf_cci")                          # Путь к папке с архивными файлами CCI
ARCHIVE_FREIGHT_DIR = os.path.join(ARCHIVE_DIR, "pdf_freight")                  # Путь к папке с архивными файлами Фрахьа
ARCHIVE_VOSTOCHNY_DIR = os.path.join(ARCHIVE_DIR, "xls_fob_vostochny")          # Путь к папке с архивными файлами FOB Vostochny
ARCHIVE_ICI3_DIR = os.path.join(ARCHIVE_DIR, "xls_ici3")                        # Путь к папке с архивными файлами ICI3
ARCHIVE_MANUAL_DIR = os.path.join(ARCHIVE_DIR, 'xlsx_manual')                   # Путь к папке с архивными файлами Ручной XLSX

# Процедура генерации директорий
def create_dirs():
    dirs_to_create = [
        FILES_DIR, ARCHIVE_DIR, DOWNLOADING_DIR,
        CCI_DIR, FREIGHT_DIR, ICI3_DIR, VOSTOCHNY_DIR, MANUAL_DIR,
        ARCHIVE_CCI_DIR, ARCHIVE_FREIGHT_DIR, ARCHIVE_VOSTOCHNY_DIR, ARCHIVE_ICI3_DIR,
        ARCHIVE_MANUAL_DIR
    ]
    
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.mkdir(dir)
            
create_dirs()