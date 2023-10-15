from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, REAL
from sqlalchemy.orm import declarative_base


# Базовый класс модели
Base = declarative_base()

# Погода в Китае
class ChinaWeather(Base):
    __tablename__ = "china_weather"
    
    # Столбцы
    cw_id = Column(INTEGER, primary_key=True, autoincrement=True)   # Первичный ключ
    update_timestamp = Column(INTEGER, nullable=False)              # Время последнего обновления строки
    date = Column(VARCHAR(10), unique=True, nullable=False)         # Дата
    beijing_temp = Column(INTEGER, nullable=False)                  # Температура в Пекине
    shanghai_temp = Column(INTEGER, nullable=False)                 # Температура в Шанхае
    guangzhou_temp = Column(INTEGER, nullable=False)                # Температура в Гуанчжоу
    nanjing_temp = Column(INTEGER, nullable=False)                  # Температура в Нанкине
    average_temp = Column(REAL, nullable=False)                     # Средняя температура по Китаю
    
    # Конструктор
    def __init__(self, date: str):
        self.date = date
    
    # Метод просчитывания средней теспературы
    def calculate_average_temp(self):
        self.average_temp = round((self.beijing_temp + self.shanghai_temp + self.guangzhou_temp + self.nanjing_temp) / 4, 1)

    # Преобразование в строку
    def __repr__(self):
        return f"<ChinaWeather({self.cw_id}, {self.date})>"
    

# Запасы CPR
class CPRStockpile(Base):
    __tablename__ = "cpr_stockpiles"
    
    # Столбцы
    cprs_id = Column(INTEGER, primary_key=True, autoincrement=True)                 # Первичный ключ
    update_timestamp = Column(INTEGER, nullable=False)                              # Время последнего обновления строки
    date = Column(VARCHAR(10), unique=True, nullable=False, default=0)              # Дата
    qinhuangdao_stockpile = Column(INTEGER, nullable=False, default=0)              # Запас в Qinhuangdao
    sdic_jingtang_stockpile = Column(INTEGER, nullable=False, default=0)            # Запас в SDIC Jingtang
    jingtang_terminal_stockpile = Column(INTEGER, nullable=False, default=0)        # Запас в Jingtang Terminal
    old_jingtang_stockpile = Column(INTEGER, nullable=False, default=0)             # Запас в Old Jingtang
    sdic_caofeidian_stockpile = Column(INTEGER, nullable=False, default=0)          # Запас в SDIC Caofeidian
    caofeidian_phase2_stockpile = Column(INTEGER, nullable=False, default=0)        # Запас в Caofeidian Phase II
    huaneng_caofeidian_stockpile = Column(INTEGER, nullable=False, default=0)       # Запас в Huaneng Caofeidian
    huadian_caofeidian_stockpile = Column(INTEGER, nullable=False, default=0)       # Запас в Huadian Caofeidian
    huanghua_stockpile = Column(INTEGER, nullable=False, default=0)                 # Запас в Huanghua
    guangzhou_stockpile = Column(INTEGER, nullable=False, default=0)                # Запас в Guangzhou
    general_stockpile = Column(INTEGER, nullable=False, default=0)                  # Общий запас
    
    # Конструктор
    def __init__(self, date: str):
        self.date = date
    
    # Метод просчитывания средней теспературы
    def calculate_general_stockpile(self):
        self.general_stockpile = self.qinhuangdao_stockpile
        self.general_stockpile += self.sdic_jingtang_stockpile
        self.general_stockpile += self.jingtang_terminal_stockpile
        self.general_stockpile += self.old_jingtang_stockpile
        self.general_stockpile += self.sdic_caofeidian_stockpile
        self.general_stockpile += self.caofeidian_phase2_stockpile
        self.general_stockpile += self.huaneng_caofeidian_stockpile
        self.general_stockpile += self.huadian_caofeidian_stockpile
        self.general_stockpile += self.huanghua_stockpile
        self.general_stockpile += self.guangzhou_stockpile

    # Преобразование в строку
    def __repr__(self):
        return f"<CPRStockpile({self.cpr_stockpile_id}, {self.date})>"


# Индексы
class Index(Base):
    __tablename__ = "indices"
    
    # Столбцы
    index_id = Column(INTEGER, primary_key=True, autoincrement=True)    # Первичный ключ
    update_timestamp = Column(INTEGER, nullable=False)                  # Время последнего обновления строки
    date = Column(VARCHAR(10), unique=True, nullable=False)             # Дата
    cci_4700 = Column(REAL, nullable=True)                              # Значение CCI 4700
    cci_4600 = Column(REAL, nullable=True)                              # Значение CCI 4600
    ici3 = Column(REAL, nullable=True)                                  # Значение ICI3
    vostochny_5500 = Column(REAL, nullable=True)                        # Значение FOB Vostochny 5500
    vostochny_4600 = Column(REAL, nullable=True)                        # # Значение FOB Vostochny 4600
    
    # Конструктор
    def __init__(self, date: str):
        self.date = date

    # Преобразование в строку
    def __repr__(self):
        return f"<Indices({self.index_id}, {self.date})>"
    

# Фрахты
class Freight(Base):
    __tablename__ = "freights"
    
    # Столбцы
    freight_id = Column(INTEGER, primary_key=True, autoincrement=True)  # Первичный ключ
    update_timestamp = Column(INTEGER, nullable=False)                  # Время последнего обновления строки
    date = Column(VARCHAR(10), unique=True, nullable=False)             # Дата
    indonesia_to_korea_rate = Column(REAL, nullable=False)              # Ставка Indonesia to Korea
    indonesia_to_india_rate = Column(REAL, nullable=False)              # Ставка Indonesia to India
    indonesia_to_china_rate = Column(REAL, nullable=False)              # Ставка Indonesia to China
    
    # Конструктор
    def __init__(self, date: str):
        self.date = date

    # Преобразование в строку
    def __repr__(self):
        return f"<Freight({self.freight_id}, {self.date})>"


# Фьючерсы
class Future(Base):
    __tablename__ = "futures"
    
    future_id = Column(INTEGER, primary_key=True, autoincrement=True)   # Первичный ключ
    update_timestamp = Column(INTEGER, nullable=False)                  # Время последнего обновления строки
    date = Column(VARCHAR(10), unique=True, nullable=False)             # Дата
    coal_last_price = Column(REAL)                                      # Последняя цена фьючерса угля
    gas_prior_settle = Column(REAL)                                     # Предварительный расчет газа
    
    # Конструктор
    def __init__(self, date: str):
        self.date = date

    # Преобразование в строку
    def __repr__(self):
        return f"<Future({self.freight_id}, {self.date})>"


# Ж/д перевозки угля
class RailCoalExport(Base):
    __tablename__ = "rail_coal_exports"
    
    rce_idf = Column(INTEGER, primary_key=True, autoincrement=True)     # Первичный ключ
    update_timestamp = Column(INTEGER, nullable=False)                  # Время последнего обновления строки
    date = Column(VARCHAR(10), unique=True, nullable=False)             # Дата
    southern_volume = Column(INTEGER)                                   # Объем Южного направления
    eastern_volume = Column(INTEGER)                                    # Объем Восточного направления
    northwestern_volume = Column(INTEGER)                               # Объем Северозападного направления
    
    # Конструктор
    def __init__(self, date: str):
        self.date = date

    # Преобразование в строку
    def __repr__(self):
        return f"<RailCoalExport({self.freight_id}, {self.date})>"