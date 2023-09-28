import os
from exchangelib import Credentials, Account, Configuration, Q, DELEGATE
from exchangelib.folders import DeletedItems
from parserlib.logger import logger
from parserlib.config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_SERVER
from parserlib.paths import cci_dir, manual_dir


# Константы
SENDER_EMAIL_ADDRESS = "noreply@ne.sxcoal.com"
SUBJECT_MANUAL_INPUT = 'manual input'
EMAIL_COUNT = 10

# Скачивает 10 последних файлов CCI из почты
def download_cci():
    logger.info("Starting CCI downloading from Email")
    
    # Создаем кренды, конфигурацию и производим вход в аккаунт
    logger.info("Making an Email account sign in")
    credentials = Credentials(EMAIL_ADDRESS, EMAIL_PASSWORD)
    config = Configuration(server=EMAIL_SERVER, auth_type='NTLM', credentials=credentials)
    exchange_account = Account(EMAIL_ADDRESS, access_type=DELEGATE, config=config)
    
    # Получаем 10 последних писем от заданного ящика
    logger.info("Receiving emails from an inbox")
    filter = Q(sender=SENDER_EMAIL_ADDRESS)
    sorted_emails = exchange_account.inbox.filter(filter).order_by('-datetime_received')[:EMAIL_COUNT]
    
    # Итерируем письма
    for email in sorted_emails:
        # Если есть вложения, начинаем итерацию вложений
        if email.attachments:
            for attachment in email.attachments:
                if attachment.content_type == 'application/pdf' and attachment.name.find("CCI Daily") != -1:
                    # Если вложение является PDF-файлом и название содержит 'CCI Daily'
                    
                    filepath = os.path.join(cci_dir, attachment.name)
                    if os.path.exists(filepath):
                        # Если файл существует, пропускаем скачивание
                        
                        logger.info(f"File '{filepath}' already exists")
                    else:
                        # Если файл не существует - скачиваем
                        
                        with open(filepath, 'wb') as f:
                            f.write(attachment.content)
                        logger.info(f"File downloaded to '{filepath}'")
                        
        # Пемерещаем письмо в корзину
        email.move_to_trash()
        
    logger.info("Done!")
    
# Скачивает 10 последних "ручных" файлов XLSX из почты
def download_manual_xlsx():
    logger.info("Starting Manual XLSX downloading from Email")
    
    # Создаем кренды, конфигурацию и производим вход в аккаунт
    logger.info("Making an Email account sign in")
    credentials = Credentials(EMAIL_ADDRESS, EMAIL_PASSWORD)
    config = Configuration(server=EMAIL_SERVER, auth_type='NTLM', credentials=credentials)
    exchange_account = Account(EMAIL_ADDRESS, access_type=DELEGATE, config=config)
    
    # Получаем 10 последних писем от заданного ящика
    logger.info("Receiving emails from an inbox")
    filter = Q(subject__iexact=SUBJECT_MANUAL_INPUT)
    sorted_emails = exchange_account.inbox.filter(filter).order_by('-datetime_received')[:EMAIL_COUNT]
    
    # Итерируем письма
    for email in sorted_emails:
        # Если есть вложения, начинаем итерацию вложений
        if email.attachments:
            for attachment in email.attachments:
                if attachment.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                    # Если вложение является XLSX-файлом
                    
                    filepath = os.path.join(manual_dir, attachment.name)
                    if os.path.exists(filepath):
                        # Если файл существует, пропускаем скачивание
                        
                        logger.info(f"File '{filepath}' already exists")
                    else:
                        # Если файл не существует - скачиваем
                        
                        with open(filepath, 'wb') as f:
                            f.write(attachment.content)
                        logger.info(f"File downloaded to '{filepath}'")
        
        # Пемерещаем письмо в корзину
        email.move_to_trash()
        
    logger.info("Done!")
    
# Точка входа
def main():
    download_cci()              # Скачиваем CCI файлы
    download_manual_xlsx()      # Скачиваем "ручной" XLSX

# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()