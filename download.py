import argparse, os
from parserlib.downloaders import argus, email
from parserlib.logger import logger
from parserlib.config import FILES_DIR
from parserlib.paths import CCI_DIR, FREIGHT_DIR, ICI3_DIR, VOSTOCHNY_DIR, DOWNLOADING_DIR


# Константы
SECTION_CHOICES = ['argus', 'email']
SECTION_HELP = "parse the section and write the data to the database"

# Создание директорий
dirs_to_create = [FILES_DIR, CCI_DIR, FREIGHT_DIR, ICI3_DIR, VOSTOCHNY_DIR, DOWNLOADING_DIR]
for dir in dirs_to_create:
    if not os.path.exists(dir):
        os.mkdir(dir)
        
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('section', help=SECTION_HELP, choices=SECTION_CHOICES)
args = arg_parser.parse_args()

try:
    if args.section == 'argus':
        argus.main()
    elif args.section == 'email':
        email.main()
except:
    logger.exception("Exception")
