import time, schedule, pytz
from parserlib.downloaders import argus, email
from parserlib.parsers import futures, gismeteo, pdf, xls
from parserlib.logger import logger


# Расписание для скачивания "ручных" файлов XLSX
schedule.every().hour.at(":00").do(email.download_manual_xlsx)      # Скачиваем "ручной" файл в :00 каждого часа
schedule.every().hour.at(":30").do(email.download_manual_xlsx)      # Скачиваем "ручной" файл в :30 каждого часа

# Расписание для парсинга "ручных" файлов XLSX
schedule.every().hour.at(":05").do(xls.parse_manual_input_files)    # Парсим "ручные" файлв в :05 каждого часа
schedule.every().hour.at(":35").do(xls.parse_manual_input_files)    # Парсим "ручные" файлв в :35 каждого часа

# Расписание для скачивания файлов CCI Daily и Argus Media
schedule.every().hour.at(":10").do(email.download_cci)              # Скачиваем CCI Daily файл в :10 каждого часа
schedule.every().hour.at(":15").do(argus.main)                      # Скачиваем файлы Argus Media в :15 каждого часа

# Расписание для парсинга файлов CCI Daily и Argus Media
schedule.every().hour.at(":20").do(pdf.main)                        # Парсим CCI Daily файлы в :20 каждого часа
schedule.every().hour.at(":25").do(xls.parse_downloaded_files)      # Парсим "скачанные" файлы в :25 каждого часа

# Расписание для парсинга погоды и фьючерсов
schedule.every().hour.at(":40").do(gismeteo.main)                   # Парсим погоду Китая в :40 каждого часа
schedule.every().hour.at(":45").do(futures.main)                    # Парсим фьючерсы в :45 каждого часа

# Точка входа
def main():
    logger.info("Service started!")
    while True:
        try:
            schedule.run_pending()
        except:
            logger.exception("Service exception:")
        finally:
            time.sleep(1)

# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()