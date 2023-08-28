import os
from parserlib import config


# Константы
CCI_DIR = os.path.join(config.FILES_DIR, "pdf_cci")
FREIGHT_DIR = os.path.join(config.FILES_DIR, "pdf_freight")
VOSTOCHNY_DIR = os.path.join(config.FILES_DIR, "xls_fob_vostochny")          # Путь к папке с файлами FOB Vostochny
ICI3_DIR = os.path.join(config.FILES_DIR, "xls_ici3")                        # Путь к папке с файлами ICI3