import os, datetime
import pandas as pd
from parserlib.db.engine import Session
from parserlib.db.model import Index
from parserlib.logger import logger
from parserlib.paths import VOSTOCHNY_DIR, ICI3_DIR



# Парсит индексы FOB Vostochny и заносит в БД
def write_vostochny_indicies(excel_file: pd.ExcelFile):
    dataframe = excel_file.parse(excel_file.sheet_names[0])[3:]     # Получаем dataframe листа
    values = dataframe.values                                       # Получаем массив строк
    
    session = Session()                                             # Открываем сессию БД
    for row in values:                                              # Итерируем строки листа
        date = row[0].strftime("%Y-%m-%d")                          # Форматируем дату для БД
        index = session.query(Index).filter_by(date=date).first()   # Ищем запись в БД по дате
        
        # Если запись не существует - создаем ее и добавляем в БД
        if not index:
            index = Index(date)
            session.add(index)
        
        # Заносим данные в сущность
        index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        index.vostochny_5500 = row[1]
        index.vostochny_4600 = round(row[1] / 5500 * 4600, 2)
        
        session.commit()                                            # Записываем данные в БД
    session.close()                                                 # Закрываем сессию БД
    
# Парсит индексы ICI3 и заносит в БД
def write_ici3_indicies(excel_file: pd.ExcelFile):
    sheet_name = excel_file.sheet_names[0]                              # Получаем название листа
    
    if sheet_name == "Price history":
        # Если открыт файл с историческими данными
        
        dataframe = excel_file.parse(sheet_name)[3:]                    # Получаем dataframe листа
        values = dataframe.values                                       # Получаем массив строк
        
        session = Session()                                             # Открываем сессию БД
        for row in values:                                              # Итерируем строки листа
            date = row[0].strftime("%Y-%m-%d")                          # Форматируем дату для БД
            index = session.query(Index).filter_by(date=date).first()   # Ищем запись в БД по дате
            
            # Если запись не существует - создаем ее и добавляем в БД
            if not index:
                index = Index(date)
                session.add(index)
            
            # Заносим данные в сущность
            index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            index.ici3 = row[2]
            
            session.commit()                                            # Записываем данные в БД
        session.close()                                                 # Закрываем сессию БД
    elif sheet_name == "Цены":
        # Если открыт файл с текущими ценами
        
        dataframe = excel_file.parse(sheet_name)                        # Получаем dataframe листа
        values = dataframe.values                                       # Получаем массив строк
        
        session = Session()                                             # Открываем сессию БД
        for row in values:                                              # Итерируем строки листа
            date = row[8].strftime("%Y-%m-%d")                          # Форматируем дату для БД
            index = session.query(Index).filter_by(date=date).first()   # Ищем запись в БД по дате
            
            # Если запись не существует - создаем ее и добавляем в БД
            if not index:
                index = Index(date)
                session.add(index)
            
            # Заносим данные в сущность
            index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            index.ici3 = row[6]
            
            session.commit()                                            # Записываем данные в БД
        session.close()                                                 # Закрываем сессию БД

# Точка входа
def main():
    logger.info("Parsing: XLS files")
    
    # Парсинг файлов FOV Vostochny
    vostochny_files = os.listdir(VOSTOCHNY_DIR)
    for filename in vostochny_files:
        logger.info(f"Parsing '{filename}' file...")
        xls_path = os.path.join(VOSTOCHNY_DIR, filename)
        excel_file = pd.ExcelFile(xls_path)
        write_vostochny_indicies(excel_file)
    
    # Парсинг файлов ICI3
    ici3_files = os.listdir(ICI3_DIR)
    for filename in ici3_files:
        logger.info(f"Parsing '{filename}' file...")
        xls_path = os.path.join(ICI3_DIR, filename)
        excel_file = pd.ExcelFile(xls_path)
        write_ici3_indicies(excel_file)
        
    logger.info("Done!")


# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()
