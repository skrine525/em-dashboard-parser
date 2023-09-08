import os, sys
from parserlib import config


# Константы
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # Путь к корневой папке приложения
CCI_DIR = os.path.join(config.FILES_DIR, "pdf_cci")                             # Путь к папке с файлами CCI
FREIGHT_DIR = os.path.join(config.FILES_DIR, "pdf_freight")                     # Путь к папке с файлами Фрахьа
VOSTOCHNY_DIR = os.path.join(config.FILES_DIR, "xls_fob_vostochny")             # Путь к папке с файлами FOB Vostochny
ICI3_DIR = os.path.join(config.FILES_DIR, "xls_ici3")                           # Путь к папке с файлами ICI3
DOWNLOADING_DIR = os.path.join(ROOT_DIR, "downloads")                           # Путь к папке с загруженными файлами