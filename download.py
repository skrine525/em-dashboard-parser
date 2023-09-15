import argparse
from parserlib.downloaders import argus, email
from parserlib.logger import logger


# Константы
SECTION_CHOICES = ['argus', 'cci', 'manual-xlsx']
SECTION_HELP = "download files of the section"
        
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('section', help=SECTION_HELP, choices=SECTION_CHOICES)
args = arg_parser.parse_args()

try:
    if args.section == 'argus':
        argus.main()
    elif args.section == 'cci':
        email.download_cci()
    elif args.section == 'manual-xlsx':
        email.download_manual_xlsx()
except:
    logger.error("Downloading error", exc_info=True)
