import argparse, os
from parserlib.parsers import features
from parserlib.parsers import gismeteo
from parserlib.parsers import pdf
from parserlib.parsers import xls
from parserlib.logger import logger
from parserlib.config import FILES_DIR
from parserlib.paths import CCI_DIR, FREIGHT_DIR, ICI3_DIR, VOSTOCHNY_DIR


# Константы
SECTION_CHOICES = ['gismeteo', 'features', 'pdf', 'xls']
SECTION_HELP = "parse the section and write the data to the database"

# Создание директорий для парсинговых файлов
parsing_dirs = [FILES_DIR, CCI_DIR, FREIGHT_DIR, ICI3_DIR, VOSTOCHNY_DIR]
for dir in parsing_dirs:
    if not os.path.exists(dir):
        os.mkdir(dir)
    
    

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('section', help=SECTION_HELP, choices=SECTION_CHOICES)
args = arg_parser.parse_args()

try:
    if args.section == 'features':
        features.main()
    elif args.section == 'gismeteo':
        gismeteo.main()
    elif args.section == 'pdf':
        pdf.main()
    elif args.section == 'xls':
        xls.main()
except:
    logger.exception("Exception")