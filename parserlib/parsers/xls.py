import os, datetime
import pandas as pd
import numpy as np
from sqlalchemy import orm
from parserlib import utils
from parserlib.db.engine import Session
from parserlib.db.model import Index, CPRStockpile, Freight, ChinaWeather, Future
from parserlib.logger import logger
from parserlib.paths import VOSTOCHNY_DIR, ICI3_DIR, MANUAL_DIR


# Парсит индексы FOB Vostochny и заносит в БД
def write_vostochny_indicies(excel_file: pd.ExcelFile, session: orm.Session):
    sheet_name = excel_file.sheet_names[0]                              # Получаем название листа
    
    if sheet_name == "Price history":
        # Если открыт файл с историческими данными
        
        dataframe = excel_file.parse(excel_file.sheet_names[0])[3:]     # Получаем dataframe листа
        values = dataframe.values                                       # Получаем массив строк
        
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
    elif sheet_name == "Цены":
        # Если открыт файл с текущими ценами
        
        dataframe = excel_file.parse(excel_file.sheet_names[0])         # Получаем dataframe листа
        values = dataframe.values                                       # Получаем массив строк
        
        for row in values:                                              # Итерируем строки листа
            date = row[8].strftime("%Y-%m-%d")                          # Форматируем дату для БД
            index = session.query(Index).filter_by(date=date).first()   # Ищем запись в БД по дате
            
            # Если запись не существует - создаем ее и добавляем в БД
            if not index:
                index = Index(date)
                session.add(index)
            
            # Заносим данные в сущность
            index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            index.vostochny_5500 = row[6]
            index.vostochny_4600 = round(row[6] / 5500 * 4600, 2)
            
            session.commit()                                            # Записываем данные в БД
    
# Парсит индексы ICI3 и заносит в БД, возвращает количество строк, прочитанных с ошибками
def write_ici3_indicies(excel_file: pd.ExcelFile, session: orm.Session) -> int:
    sheet_name = excel_file.sheet_names[0]                              # Получаем название листа
    
    if sheet_name == "Price history":
        # Если открыт файл с историческими данными
        
        dataframe = excel_file.parse(sheet_name)[3:]                    # Получаем dataframe листа
        values = dataframe.values                                       # Получаем массив строк
        
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
    elif sheet_name == "Цены":
        # Если открыт файл с текущими ценами
        
        dataframe = excel_file.parse(sheet_name)                        # Получаем dataframe листа
        values = dataframe.values                                       # Получаем массив строк
        
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
        
# Парсит и записывает данные в БД из "ручного" файла
def write_manual_input(excel_file: pd.ExcelFile, session: orm.Session):
    # Парсим Index
    dataframe = excel_file.parse("Index")                               # Получаем dataframe листа
    values = dataframe.values                                           # Получаем массив строк
    
    for row in values:
        try:
            date = row[0].strftime("%Y-%m-%d")                              # Форматируем дату для БД
            cci_4700 = float(row[1])                                        # Получаем поле "CCI 4700"
            ici3 = float(row[2])                                            # Получаем поле "ICI3"
            vostochny_5500 = float(row[3])                                  # Получаем поле "FOB Vostochny 5500"
            update = False if np.isnan(row[4]) else bool(int(row[4]))       # Получаем поле "Обновить?"
            
            index = session.query(Index).filter_by(date=date).first()       # Ищем запись в БД по дате
            
            if not index:
                # Если запись не существует - добавляем ее
                index = Index(date)
                session.add(index)
            elif not update:
                # Если запись существует и обновлять запись не нужно - пропускаем
                continue
            
            # Заносим данные в сущность
            index.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            index.cci_4700 = cci_4700
            index.cci_4600 = round(index.cci_4700 / 4700 * 4600, 2)
            index.ici3 = ici3
            index.vostochny_5500 = vostochny_5500
            index.vostochny_4600 = round(index.vostochny_5500 / 5500 * 4600, 2)
            
            session.commit()                                                # Записываем данные в БД
        except:
            row_str = str(row)
            logger.exception(f"Exception from parsing row of sheet 'Index': {row_str}")
        
    # Парсим CPR Stockpile
    dataframe = excel_file.parse("CPR Stockpile")                                           # Получаем dataframe листа
    values = dataframe.values                                                               # Получаем массив строк
    
    for row in values:
        try:
            date = row[0].strftime("%Y-%m-%d")                                              # Форматируем дату для БД
            qinhuangdao_stockpile = int(row[1])                                             # Получаем поле "Qinhuangdao"
            sdic_jingtang_stockpile = int(row[2])                                           # Получаем поле "SDIC Jingtang"
            jingtang_terminal_stockpile = int(row[3])                                       # Получаем поле "Jingtang Terminal"
            old_jingtang_stockpile = int(row[4])                                            # Получаем поле "Old Jingtang"
            sdic_caofeidian_stockpile = int(row[5])                                         # Получаем поле "SDIC Caofeidian"
            caofeidian_phase2_stockpile = int(row[6])                                       # Получаем поле "Caofeidian Phase II"
            huaneng_caofeidian_stockpile = int(row[7])                                      # Получаем поле "Huaneng Caofeidian"
            huanghua_stockpile = int(row[8])                                                # Получаем поле "Huanghua"
            guangzhou_stockpile = int(row[9])                                               # Получаем поле "Guangzhou"
            update = False if np.isnan(row[10]) else bool(int(row[10]))                     # Получаем поле "Обновить?"
            
            cpr_stockpile = session.query(CPRStockpile).filter_by(date=date).first()
            
            if not cpr_stockpile:
                # Если запись не существует - добавляем ее
                cpr_stockpile = CPRStockpile(date)
                session.add(cpr_stockpile)
            elif not update:
                # Если запись существует и обновлять запись не нужно - пропускаем
                continue
            
            # Заносим данные в сущность
            cpr_stockpile.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            cpr_stockpile.qinhuangdao_stockpile = qinhuangdao_stockpile
            cpr_stockpile.sdic_jingtang_stockpile = sdic_jingtang_stockpile
            cpr_stockpile.jingtang_terminal_stockpile = jingtang_terminal_stockpile
            cpr_stockpile.old_jingtang_stockpile = old_jingtang_stockpile
            cpr_stockpile.sdic_caofeidian_stockpile = sdic_caofeidian_stockpile
            cpr_stockpile.caofeidian_phase2_stockpile = caofeidian_phase2_stockpile
            cpr_stockpile.huaneng_caofeidian_stockpile = huaneng_caofeidian_stockpile
            cpr_stockpile.huanghua_stockpile = huanghua_stockpile
            cpr_stockpile.guangzhou_stockpile = guangzhou_stockpile
            cpr_stockpile.calculate_general_stockpile()
            
            session.commit()                                                                # Записываем данные в БД
        except:
            row_str = str(row)
            logger.exception(f"Exception from parsing row of sheet 'CPR Stockpile': {row_str}")
            
    # Парсим Freight
    dataframe = excel_file.parse("Freight")                                                 # Получаем dataframe листа
    values = dataframe.values                                                               # Получаем массив строк
    
    for row in values:
        try:
            date = row[0].strftime("%Y-%m-%d")                                              # Форматируем дату для БД
            indonesia_to_korea_rate = float(row[1])                                         # Получаем поле "Indonesia to Korea"
            indonesia_to_india_rate = float(row[2])                                         # Получаем поле "Indonesia to India"
            indonesia_to_china_rate = float(row[3])                                         # Получаем поле "Indonesia to China"
            update = False if np.isnan(row[4]) else bool(int(row[4]))                       # Получаем поле "Обновить?"
            
            freight = session.query(Freight).filter_by(date=date).first()                   # Ищем запись в БД по дате
            
            if not freight:
                # Если запись не существует - добавляем ее
                freight = Freight(date)
                session.add(freight)
            elif not update:
                # Если запись существует и обновлять запись не нужно - пропускаем
                continue
            
            # Заносим данные в сущность
            freight.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            freight.indonesia_to_korea_rate = indonesia_to_korea_rate
            freight.indonesia_to_india_rate = indonesia_to_india_rate
            freight.indonesia_to_china_rate = indonesia_to_china_rate
            
            session.commit()                                                                # Записываем данные в БД
        except:
            row_str = str(row)
            logger.exception(f"Exception from parsing row of sheet 'Freight': {row_str}")
            
    # Парсим Futures
    dataframe = excel_file.parse("Futures")                                                 # Получаем dataframe листа
    values = dataframe.values                                                               # Получаем массив строк
    
    for row in values:
        try:
            date = row[0].strftime("%Y-%m-%d")                                              # Форматируем дату для БД
            coal_last_price = float(row[1])                                                 # Получаем поле "Coal Last Price"
            gas_prior_settle = float(row[2])                                                # Получаем поле "Gas Prior Settle"
            update = False if np.isnan(row[3]) else bool(int(row[3]))                       # Получаем поле "Обновить?"
            
            future = session.query(Future).filter_by(date=date).first()                     # Ищем запись в БД по дате
            
            if not future:
                # Если запись не существует - добавляем ее
                future = Future(date)
                session.add(future)
            elif not update:
                # Если запись существует и обновлять запись не нужно - пропускаем
                continue
            
            # Заносим данные в сущность
            future.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            future.coal_last_price = coal_last_price
            future.gas_prior_settle = gas_prior_settle
            
            session.commit()                                                                # Записываем данные в БД
        except:
            row_str = str(row)
            logger.exception(f"Exception from parsing row of sheet 'Futures': {row_str}")
            
    # Парсим Futures
    dataframe = excel_file.parse("China Weather")                                           # Получаем dataframe листа
    values = dataframe.values                                                               # Получаем массив строк
    
    for row in values:
        try:
            date = row[0].strftime("%Y-%m-%d")                                              # Форматируем дату для БД
            beijing_temp = float(row[1])                                                    # Получаем поле "Beijing Temp."
            shanghai_temp = float(row[2])                                                   # Получаем поле "Shanghai Temp."
            guangzhou_temp = float(row[3])                                                  # Получаем поле "Guangzhou Temp."
            nanjing_temp = float(row[4])                                                    # Получаем поле "Nanjing Temp."
            update = False if np.isnan(row[5]) else bool(int(row[5]))                       # Получаем поле "Обновить?"
            
            china_weather = session.query(ChinaWeather).filter_by(date=date).first()        # Ищем запись в БД по дате
            
            if not china_weather:
                # Если запись не существует - добавляем ее
                china_weather = ChinaWeather(date)
                session.add(china_weather)
            elif not update:
                # Если запись существует и обновлять запись не нужно - пропускаем
                continue
            
            # Заносим данные в сущность
            china_weather.update_timestamp = int(datetime.datetime.utcnow().timestamp())
            china_weather.beijing_temp = beijing_temp
            china_weather.guangzhou_temp = guangzhou_temp
            china_weather.shanghai_temp = shanghai_temp
            china_weather.nanjing_temp = nanjing_temp
            china_weather.calculate_average_temp()
            
            session.commit()                                                                # Записываем данные в БД
        except:
            row_str = str(row)
            logger.exception(f"Exception from parsing row of sheet 'Futures': {row_str}")
        
# Записывает данные в БД из "ручных" XLSX файлов
def parse_manual_input_files():
    session = Session()                                                     # Открываем сессию БД
    
    try:
        logger.info("Parsing: Manual XLSX files")
        
        # Парсим "ручные" XLSX файлы
        manual_files = os.listdir(MANUAL_DIR)
        for filename in manual_files:
            logger.info(f"Parsing '{filename}' file")
            
            try:
                # Открываем файл
                xlsx_path = os.path.join(MANUAL_DIR, filename)
                excel_file = pd.ExcelFile(xlsx_path)
                
                # Парсим файл и закрываем его
                write_manual_input(excel_file, session)
                excel_file.close()
                
                utils.archive_file(xlsx_path)
            except:
                logger.exception(f"File '{filename}' parsing exception")
        
        logger.info("Done!")
    finally:
        session.close()                                                     # Закрываем сессию БД
    
# Записывает данные в БД из скачанных файлов
def parse_downloaded_files():
    session = Session()                                                     # Открываем сессию БД
    
    try:
        logger.info("Parsing: XLS files")
        
        # Парсинг файлов FOV Vostochny
        vostochny_files = os.listdir(VOSTOCHNY_DIR)
        for filename in vostochny_files:
            logger.info(f"Parsing '{filename}' file")
            
            try:# Открываем файл
                xls_path = os.path.join(VOSTOCHNY_DIR, filename)
                excel_file = pd.ExcelFile(xls_path)
                
                # Парсим файл и закрываем его
                write_vostochny_indicies(excel_file, session)
                excel_file.close()
                
                utils.archive_file(xls_path)
            except:
                logger.exception(f"File '{filename}' parsing exception")
        
        # Парсинг файлов ICI3
        ici3_files = os.listdir(ICI3_DIR)
        for filename in ici3_files:
            logger.info(f"Parsing '{filename}' file")
            
            try:
                # Открываем файл
                xls_path = os.path.join(ICI3_DIR, filename)
                excel_file = pd.ExcelFile(xls_path)
                
                # Парсим файл и закрываем его
                write_ici3_indicies(excel_file, session)
                excel_file.close()
                
                utils.archive_file(xls_path)
            except:
                logger.exception(f"File '{filename}' parsing exception")
            
        logger.info("Done!")
    finally:
        session.close()                                                     # Закрываем сессию БД

# Точка входа
def main():
    parse_downloaded_files()
    parse_manual_input_files()

# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()
