import argparse, os
from parserlib.downloaders import argus, email
from parserlib.logger import logger


# Константы
SECTION_CHOICES = ['argus', 'email']
SECTION_HELP = "parse the section and write the data to the database"
        
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('section', help=SECTION_HELP, choices=SECTION_CHOICES)
args = arg_parser.parse_args()

try:
    if args.section == 'argus':
        argus.main()
    elif args.section == 'email':
        email.main()
except:
    logger.error("Downloading error", exc_info=True)
