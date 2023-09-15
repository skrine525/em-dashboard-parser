import os, datetime, fitz, pytesseract
from sqlalchemy import orm
from PIL import Image
from io import BytesIO
from PyPDF2 import PdfReader
from parserlib import utils
from parserlib.db.model import CPRStockpile, Index, Freight
from parserlib.db.engine import Session
from parserlib.logger import logger
from parserlib.paths import CCI_DIR, FREIGHT_DIR


# Константы
CCI_STRING = "CCI 4700 Import^"
CCI_STRING_V2 = "cci 4700 import"
CCI_CHINA_STRING = 'china'
STOCKPILE_STRING = "Stockpile"
FREIGHT_STRING_1 = "Indonesia-S Korea"
FREIGHT_STRING_2 = "Indonesia-EC India"
FREIGHT_STRING_3 = "Indonesia-S China"
MONTHS = [
    ['Jan', 1, '01'],
    ['Feb', 2, '02'],
    ['Mar', 3, '03'],
    ['Apr', 4, '04'],
    ['May', 5, '05'],
    ['Jun', 6, '06'],
    ['Jul', 7, '07'],
    ['Aug', 8, '08'],
    ['Sep', 9, '09'],
    ['Ocr', 10, '10'],
    ['Nov', 11, '11'],
    ['Dec', 12, '12'],
]

# Возвращает строку с датой, полученной из названия файла CCI
def get_date_by_cci_filename(filename: str) -> str:
    i = filename.find("(") + 1
    j = filename.find(")", i)
    date_from_filename = filename[i:j].replace(',', '')
    splitted_date_from_filename = date_from_filename.split()

    day_str = splitted_date_from_filename[1]
    day_str = day_str = f"0{day_str}" if int(day_str) < 10 else day_str
    year_str = splitted_date_from_filename[2]

    for month in MONTHS:
        if month[0] == splitted_date_from_filename[0]:
            month_str = month[2]

    return f"{year_str}-{month_str}-{day_str}"

# Возвращает строку с датой, полученной из названия файла Freight
def get_date_by_freight_filename(filename: str) -> str:
    i = filename.find("_")
    fused_date = filename[:i]

    # Получаем год, месяц и день
    year = fused_date[:4]
    month = fused_date[4:6]
    day = fused_date[6:]

    return f"{year}-{month}-{day}"

# Извлекает текст из всех картинок PDF файла
def extract_text_from_images_in_pdf(pdf_path) -> str:
    pdf_document = fitz.open(pdf_path)
    
    text = ''
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_data = base_image["image"]
            
            # Создаем объект BytesIO для чтения данных изображения
            image_stream = BytesIO(image_data)

            # Открываем изображение с помощью Pillow
            image = Image.open(image_stream)
            
            custom_config = r'--oem 3 --psm 6'  # Опции для распознавания (с права налево, сверху вниз)
            text += pytesseract.image_to_string(image, config=custom_config, lang='eng')
    
    pdf_document.close()
    return text

# Парсит данные о запасах CPR и записывает в базу данных ПЕРВЫМ способом
def write_stockpiles(reader: PdfReader, session: orm.Session, date: str):
    cpr_stockpile = session.query(CPRStockpile).filter_by(date=date).first()    # Ищем запись в БД по дате

    if not cpr_stockpile:                                           # Если запись не существует, начинаем парсинг
        page = reader.pages[4]                                      # Открываем пятую страницу файла
        text = page.extract_text().replace("\n", " ")               # Достаем текст из страницы
        
        # Парсим запасы
        try:
            stockpiles = []
            i = 0
            while len(stockpiles) < 9:
                i = text.find(STOCKPILE_STRING, i + 1)              # Получаем индекс первого символа Stockpile
                j = i + len(STOCKPILE_STRING) + 1                   # Просчитываем первый символ числа
                k = text.find(' ', j)                               # Просчитываем индекс пробела после числа
                stockpile_str = text[j:k]                           # Извлекаем число в виде строки
                stockpile_str = stockpile_str.replace(',', '')      # Избавляемся от запятой в строке
                stockpile = int(float(stockpile_str))               # Получаем числовую переменную из строки
                stockpiles.append(stockpile)                        # Заносим число в список
        except ValueError:
            return "Error"
        
        # Создаем и добавляем запись в БД
        cpr_stockpile = CPRStockpile(date)
        session.add(cpr_stockpile)
        
        # Записываем данные в сущность
        cpr_stockpile.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        cpr_stockpile.qinhuangdao_stockpile = stockpiles[0]
        cpr_stockpile.sdic_jingtang_stockpile = stockpiles[1]
        cpr_stockpile.jingtang_terminal_stockpile = stockpiles[2]
        cpr_stockpile.old_jingtang_stockpile = stockpiles[3]
        cpr_stockpile.sdic_caofeidian_stockpile = stockpiles[4]
        cpr_stockpile.caofeidian_phase2_stockpile = stockpiles[5]
        cpr_stockpile.huaneng_caofeidian_stockpile = stockpiles[6]
        cpr_stockpile.huanghua_stockpile = stockpiles[7]
        cpr_stockpile.guangzhou_stockpile = stockpiles[8]
        cpr_stockpile.calculate_general_stockpile()

        session.commit()                                            # Записываем данные в БД

        return "Added"
    else:                                                           # Если запись существует, пропускаем парсинг
        return "Skipped"
    
# Парсит данные о запасах CPR и записывает в базу данных ВТОРЫМ способом
def write_stockpiles_v2(text: str, session: orm.Session, date: str):
    cpr_stockpile = session.query(CPRStockpile).filter_by(date=date).first()    # Ищем запись в БД по дате

    if not cpr_stockpile:                                           # Если запись не существует, начинаем парсинг
        # Парсим запасы
        try:
            stockpiles = []
            i = 0
            while len(stockpiles) < 9:
                i = text.find(STOCKPILE_STRING.lower(), i + 1)      # Получаем индекс первого символа Stockpile
                j = i + len(STOCKPILE_STRING) + 1                   # Просчитываем первый символ числа
                k = text.find(' ', j)                               # Просчитываем индекс пробела после числа
                stockpile_str = text[j:k]                           # Извлекаем число в виде строки
                stockpile_str = stockpile_str.replace(',', '')      # Избавляемся от запятой в строке
                stockpile = int(float(stockpile_str))               # Получаем числовую переменную из строки
                stockpiles.append(stockpile)                        # Заносим число в список
        except ValueError:
            return "Error"
        
        # Создаем и добавляем запись в БД
        cpr_stockpile = CPRStockpile(date)
        session.add(cpr_stockpile)
        
        # Записываем данные в сущность
        cpr_stockpile.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        cpr_stockpile.qinhuangdao_stockpile = stockpiles[0]
        cpr_stockpile.sdic_jingtang_stockpile = stockpiles[1]
        cpr_stockpile.jingtang_terminal_stockpile = stockpiles[2]
        cpr_stockpile.old_jingtang_stockpile = stockpiles[3]
        cpr_stockpile.sdic_caofeidian_stockpile = stockpiles[4]
        cpr_stockpile.caofeidian_phase2_stockpile = stockpiles[5]
        cpr_stockpile.huaneng_caofeidian_stockpile = stockpiles[6]
        cpr_stockpile.huanghua_stockpile = stockpiles[7]
        cpr_stockpile.guangzhou_stockpile = stockpiles[8]
        cpr_stockpile.calculate_general_stockpile()

        session.commit()                                            # Записываем данные в БД

        return "Added"
    else:                                                           # Если запись существует, пропускаем парсинг
        return "Skipped"

# Парсит и записывает CCI индексы в базу данных ПЕРВЫМ способом
def write_cci_indicies(reader: PdfReader, session: orm.Session, date: str):
    index = session.query(Index).filter_by(date=date).first()       # Ищем запись в БД по дате

    if not index:                                                   # Если запись не сущесвует - создаем и добавляем в БД
        index = Index(date)
        session.add(index)

    if not index.cci_4600 or not index.cci_4700:                    # Если один из индексов не заполнен, то начинаем парсинг
        page = reader.pages[0]                                      # Открываем первую страницу
        text = page.extract_text().replace("\n", " ")               # Достаем текст из страницы
        
        # Парсим индекс
        i = text.find(CCI_STRING, 0)
        j = i + len(CCI_STRING) + 1
        k = text.find(' ', j)
        cci_4700_str = text[j:k]

        try:
            # Заносим данные в сущность
            index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            index.cci_4700 = float(cci_4700_str)
            index.cci_4600 = round(index.cci_4700 / 4700 * 4600, 2)
            
            session.commit()            # Записываем данные в БД

            return "Added"
        except ValueError:
            session.rollback()
            return "Error"
    else:                                                           # Если все индексы заполнены - пропускаем парсинг
        return "Skipped"
    
# Парсит и записывает CCI индексы в базу данных ВТОРЫМ способом
def write_cci_indicies_v2(text: str, session: orm.Session, date: str):
    index = session.query(Index).filter_by(date=date).first()       # Ищем запись в БД по дате

    if not index:                                                   # Если запись не сущесвует - создаем и добавляем в БД
        index = Index(date)
        session.add(index)

    if not index.cci_4600 or not index.cci_4700:                    # Если один из индексов не заполнен, то начинаем парсинг
        text = text.replace("\n", " ")                              # Заменяем символ перехода строки на пробел
        
        # Парсим индекс
        i = text.find(CCI_STRING_V2, 0)
        i = text.find(CCI_CHINA_STRING, i + 1)
        j = i + len(CCI_CHINA_STRING) + 1
        k = text.find(' ', j)
        cci_4700_str = text[j:k]

        try:
            # Заносим данные в сущность
            index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            index.cci_4700 = float(cci_4700_str)
            index.cci_4600 = round(index.cci_4700 / 4700 * 4600, 2)
            
            session.commit()            # Записываем данные в БД

            return "Added"
        except ValueError:
            session.rollback()
            return "Error"
    else:                                                           # Если все индексы заполнены - пропускаем парсинг
        return "Skipped"

# Парсит данные о фрахтах и записывает в базу данных
def write_freight(reader: PdfReader, session: orm.Session, date: str = None):
    freight = session.query(Freight).filter_by(date=date).first()   # Ищем запись в БД по дате

    if not freight:                                                 # Если запись не существует - начинаем парсинг
        # Создаем и добавляем в БД
        freight = Freight(date)
        freight.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        session.add(freight)

        page = reader.pages[2]                                      # Открываем первую страницу
        text = page.extract_text().replace("\n", " ")               # Достаем текст из страницы

        try:
            # Indonesia-S Korea rate
            i = text.find(FREIGHT_STRING_1, 0)                      # Получаем индекс начала слова
            j = text.find("Coal", i) + 5                            # Просчитываем положение первого символа числа
            k = text.find(' ', j)                                   # Просчитываем положение пробела после числа
            freight.indonesia_to_korea_rate = float(text[j:k])      # Получаем число

            # Indonesia-EC India rate
            i = text.find(FREIGHT_STRING_2, 0)                      # Получаем индекс начала слова
            j = text.find("Coal", i) + 5                            # Просчитываем положение первого символа числа                          
            k = text.find(' ', j)                                   # Просчитываем положение пробела после числа
            freight.indonesia_to_india_rate = float(text[j:k])      # Получаем число

            # Indonesia-S China rate
            i = text.find(FREIGHT_STRING_3, 0)                      # Получаем индекс начала слова
            j = text.find("Coal", i) + 5                            # Просчитываем положение первого символа числа
            k = text.find(' ', j)                                   # Просчитываем положение пробела после числа
            freight.indonesia_to_china_rate = float(text[j:k])      # Получаем число

            session.commit()                                        # Записываем данные в БД

            return 'Added'
        except ValueError:
            session.rollback()
            return "Error"
    else:
        return "Skipped"

# Точка входа
def main():
    session = Session()
    
    try:
        logger.info("Parsing: PDF files")
        
        # Получаем список файлов CCI
        pdf_files = os.listdir(CCI_DIR)
        sorted_pdf_files = []
        for filename in pdf_files:
            # Просчитываем дату из названия файла
            date = get_date_by_cci_filename(filename)
            sorted_pdf_files.append([filename, date])

        # Выполняем сортировку файлов по дате
        n = len(sorted_pdf_files)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_pdf_files[j][1] > sorted_pdf_files[j + 1][1]:
                    sorted_pdf_files[j], sorted_pdf_files[j + 1] = sorted_pdf_files[j + 1], sorted_pdf_files[j]
                    
        # Итерируем файлы и парсим 
        for file_data in sorted_pdf_files:
            try:
                pdf_path = os.path.join(CCI_DIR, file_data[0])                                          # Формируем путь к файлу
                reader = PdfReader(pdf_path)                                                            # Создаем "читателя" файла
                page1_text = reader.pages[0].extract_text()                                             # Достаем текст из первой страницы страницы
                i = page1_text.find(' ')
                first_word = page1_text[:i].lower()
                
                # Определяем тип файла: новый или старый
                if first_word == 'cci':
                    # Новый файл, используем второй вариант парсинга
                    
                    text = extract_text_from_images_in_pdf(pdf_path).lower()                            # Извлекаем текст из картинок в PDF файле
                    result_stockpiles = write_stockpiles_v2(text, session, file_data[1])                # Парсим запасы
                    result_cci = write_cci_indicies_v2(text, session, file_data[1])                     # Парсим индексы
                    
                    logger.info(f"Parsing '{file_data[0]}' file: [Stockpiles {result_stockpiles}]")
                    logger.info(f"Parsing '{file_data[0]}' file: [CCI {result_cci}]")
                    
                    if result_stockpiles != "Error" and result_cci != 'Error':
                        utils.archive_file(pdf_path)
                else:
                    # Старый файл, используем первый вариант парсинга
                    
                    result_stockpiles = write_stockpiles(reader, session, file_data[1])                 # Парсим запасы
                    result_cci = write_cci_indicies(reader, session, file_data[1])                      # Парсим индексы
                    
                    logger.info(f"Parsing '{file_data[0]}' file: [Stockpiles {result_stockpiles}]")
                    logger.info(f"Parsing '{file_data[0]}' file: [CCI {result_cci}]")
                    
                    if result_stockpiles != "Error" and result_cci != 'Error':
                        utils.archive_file(pdf_path)
            except:
                logger.exception(f"File '{file_data[0]}' parsing exception")

        # Получаем список файлов Freight
        pdf_files = os.listdir(FREIGHT_DIR)
        sorted_pdf_files = []
        for filename in pdf_files:
            # Просчитываем дату из названия файла
            date = get_date_by_freight_filename(filename)
            sorted_pdf_files.append([filename, date])

        # Выполняем сортировку файлов по дате
        n = len(sorted_pdf_files)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_pdf_files[j][1] > sorted_pdf_files[j + 1][1]:
                    sorted_pdf_files[j], sorted_pdf_files[j + 1] = sorted_pdf_files[j + 1], sorted_pdf_files[j]
        
        # Итерируем файлы и парсим 
        for file_data in sorted_pdf_files:
            try:
                pdf_path = os.path.join(FREIGHT_DIR, file_data[0])                                  # Формируем путь к файлу
                reader = PdfReader(pdf_path)                                                        # Создаем "читателя" файла
                
                result = write_freight(reader, session, file_data[1])                               # Парсим запасы
                logger.info(f"Parsing '{file_data[0]}' file: [Freight {result}]")
                
                if result != "Error":
                    utils.archive_file(pdf_path)
            except:
                logger.exception(f"File '{file_data[0]}' parsing exception")
            
        logger.info("Done!")
    finally:
        session.close()

# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()
