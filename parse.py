import argparse
from parserlib.parsers import futures
from parserlib.parsers import gismeteo
from parserlib.parsers import pdf
from parserlib.parsers import xls
from parserlib.logger import logger


# Константы
SECTION_CHOICES = ['gismeteo', 'futures', 'pdf', 'xls', 'manual-xlsx']
SECTION_HELP = "parse the section and write the data to the database"

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('section', help=SECTION_HELP, choices=SECTION_CHOICES)
args = arg_parser.parse_args()

try:
    if args.section == 'futures':
        futures.main()
    elif args.section == 'gismeteo':
        gismeteo.main()
    elif args.section == 'pdf':
        pdf.main()
    elif args.section == 'xls':
        xls.parse_downloaded_files()
    elif args.section == 'manual-xlsx':
        xls.parse_manual_input_files()
except:
    logger.error("Parsing error", exc_info=True)
