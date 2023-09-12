import argparse, os
from parserlib.parsers import features
from parserlib.parsers import gismeteo
from parserlib.parsers import pdf
from parserlib.parsers import xls
from parserlib.logger import logger


# Константы
SECTION_CHOICES = ['gismeteo', 'features', 'pdf', 'xls']
SECTION_HELP = "parse the section and write the data to the database"

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
    logger.error("Parsing error", exc_info=True)
