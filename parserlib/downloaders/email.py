import os
from exchangelib import Credentials, Account, Configuration, Q, DELEGATE
from parserlib.logger import logger
from parserlib.config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_SERVER
from parserlib.paths import DOWNLOADING_DIR, CCI_DIR


# Константы
SENDER_EMAIL_ADDRESS = "noreply@ne.sxcoal.com"
EMAIL_COUNT = 10

# Точка входа
def main():
    logger.info("Starting Email downloading")
    
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
        print(f"Subject: {email.subject}")
        print(f"From: {email.sender.email_address}")
        print(f"Received: {email.datetime_received}")
        print("\n")
        
        # Если есть вложения, начинаем итерацию вложений
        if email.attachments:
            for attachment in email.attachments:
                if attachment.content_type == 'application/pdf' and attachment.name.find("CCI Daily") != -1:
                    # Если вложение является PDF-файлом и название содержит 'CCI Daily'
                    
                    filepath = os.path.join(CCI_DIR, attachment.name)
                    if os.path.exists(filepath):
                        # Если файл существует, пропускаем скачивание
                        
                        logger.info(f"File '{filepath}' already exists")
                    else:
                        # Если файл не существует - скачиваем
                        
                        with open(filepath, 'wb') as f:
                            f.write(attachment.content)
                        logger.info(f"File downloaded to '{filepath}'")
        
    logger.info("Done!")

# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()