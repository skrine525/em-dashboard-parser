import os

# Переменные
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # Путь к корневой папке приложения
downloading_dir = os.path.join(root_dir, "downloads")                           # Путь к папке с загруженными файлами
files_dir = os.path.join(root_dir, "files")                                     # Путь к корневой папке парсинга
archive_dir = os.path.join(files_dir, 'archive')                                # Путь к папке архивных файлов
cci_dir = os.path.join(files_dir, "pdf_cci")                                    # Путь к папке с файлами CCI
freight_dir = os.path.join(files_dir, "pdf_freight")                            # Путь к папке с файлами Фрахьа
vostochny_dir = os.path.join(files_dir, "xls_fob_vostochny")                    # Путь к папке с файлами FOB Vostochny
ici3_dir = os.path.join(files_dir, "xls_ici3")                                  # Путь к папке с файлами ICI3
manual_dir = os.path.join(files_dir, 'xlsx_manual')                             # Путь к папке с файлами Ручной XLSX
archive_cci_dir = os.path.join(archive_dir, "pdf_cci")                          # Путь к папке с архивными файлами CCI
archive_freight_dir = os.path.join(archive_dir, "pdf_freight")                  # Путь к папке с архивными файлами Фрахьа
archive_vostochny_dir = os.path.join(archive_dir, "xls_fob_vostochny")          # Путь к папке с архивными файлами FOB Vostochny
archive_ici3_dir = os.path.join(archive_dir, "xls_ici3")                        # Путь к папке с архивными файлами ICI3
archive_manual_dir = os.path.join(archive_dir, 'xlsx_manual')                   # Путь к папке с архивными файлами Ручной XLSX
config_file = os.path.join(root_dir, 'config.json')                             # Путь к конфигурационному файлу
log_file  = os.path.join(root_dir, 'parser.log')                                # Путь к файлу логов

# Функция генерации директорий
def create_dirs():
    dirs_to_create = [
        files_dir, archive_dir, downloading_dir,
        cci_dir, freight_dir, ici3_dir, vostochny_dir, manual_dir,
        archive_cci_dir, archive_freight_dir, archive_vostochny_dir, archive_ici3_dir,
        archive_manual_dir
    ]
    
    for dir in dirs_to_create:
        if not os.path.exists(dir):
            os.mkdir(dir)
            
create_dirs()       # Создаем директории