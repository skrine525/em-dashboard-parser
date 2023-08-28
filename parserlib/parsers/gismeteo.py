import urllib.request, time, pytz, datetime
from bs4 import BeautifulSoup as bs
from parserlib.db.engine import Session
from parserlib.db.model import ChinaWeather
from parserlib.logger import logger


# Константы
MONTHS = [
    ['янв', 1, '01'],
    ['фев', 2, '02'],
    ['мар', 3, '03'],
    ['апр', 4, '04'],
    ['май', 5, '05'],
    ['июн', 6, '06'],
    ['июл', 7, '07'],
    ['авг', 8, '08'],
    ['сен', 9, '09'],
    ['окт', 10, '10'],
    ['ноя', 11, '11'],
    ['дек', 12, '12'],
]
REGIONS = [
    ['Beijing', 'weather-beijing-6355', '6355'],
    ['Shanghai', 'weather-shanghai-6408', '6408'],
    ['Guangzhou', 'weather-guangzhou-6455', '6455'],
    ['Nanjing', 'weather-nanjing-lukou-30546', '30546']
]

# Возвращает параметры месяца по тектовому сокращению
def get_month_by_str(m: str) -> int:
    for month in MONTHS:
        if month[0] == m:
            return month
    return None

# Вовзаращет истроию о погоде на промежутке дат
def get_gismeteio_diary(city: str, start: tuple, end: tuple, interval: float = 1):
    # Настройка HTTP запроса
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}

    for year in range(start[0], end[0] + 1):    # Итерируем года
        # Формируем диапазон начального и конечного месяца на год
        month_range_start = 1
        month_range_end = 13
        if year == start[0]:
            month_range_start = start[1]
        if year == end[0]:
            month_range_end = end[1] + 1

        data = []   # Массив, хранящий словарь из date и temp
        for month in range(month_range_start, month_range_end):             # Итерируем месяца
            url = f"https://www.gismeteo.ru/diary/{city}/{year}/{month}"    # Формируем URL на дневник
            req = urllib.request.Request(url, headers=headers)              # Инициируем запрос
            with urllib.request.urlopen(req) as response:                   # Делаем запрос
                page = response.read()                                      # Получаем HTML страницы
                soup = bs(page, "html.parser")                              # Создаем объект парсера 

                table = soup.find('table')                                  # Ищем таблицу
                tbody = table.find('tbody')                                 # Ищем тело таблицы
                tr_list = tbody.find_all('tr')                              # Ищем все строки таблицы
                for tr in tr_list:                                          # Итерируем строки таблицы
                    td_list = tr.find_all('td')                             # Ищем все столбцы строки
                    
                    # Парсим и форматируем день
                    day = td_list[0].contents[0]                                  
                    day = f"0{day}" if len(day) < 2 else day
                    
                    # Парсим дневную и ночную температуры
                    temp_day = float(td_list[1].contents[0]) if isinstance(td_list[1].contents[0], str) else 0
                    temp_night = float(td_list[6].contents[0]) if isinstance(td_list[6].contents[0], str) else 0
                    
                    # Формируем дату и находим среднюю температуру
                    date = f'{year}-{MONTHS[month - 1][2]}-{day}'
                    temp = round((temp_day + temp_night) / 2, 2)
                    
                    data.append({"date": date, "temp": temp})   # Заносим словарь в список

            time.sleep(interval)    # Задержка между запросами

        return data


# Возвращает данные о погоде на месяц по заданному городу
def get_gismeteo_month(city_url: str) -> list:
    # Настройка HTTP запроса
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    headers = {'User-Agent': user_agent}
    url = f"https://www.gismeteo.ru/{city_url}/month"
    req = urllib.request.Request(url, headers=headers)

    data = []                                       # Массив, хранящий словарь из date и temp
    with urllib.request.urlopen(req) as response:   # Делаем запрос
        page = response.read()                      # Получаем HTML страницы
        soup = bs(page, "html.parser")              # Создаем объект парсера 

        items = soup.find_all('a', class_='row-item')                                       # Ищем элементы погоды
        current_moscow_datetime = datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))  # Получаем текущую дату по МСК
        current_month = None                                                                # Текущий месяц
        current_year = current_moscow_datetime.year                                         # Текущий год
        for item in items:
            date = item.find("div", class_="date", recursive=False).contents[0]             # Находим дату

            # Находим максимальную температуру и парсим
            temp_item = item.find('div', class_="maxt").find("span", class_="unit")
            try:
                factor = 1 if temp_item.contents[0].contents[0] == "+" else -1
            except IndexError:
                factor = 1
            temp = factor * int(temp_item.contents[1])

            # Находим минимальную температуру, парсим и считаем среднее значение
            temp_item = item.find('div', class_="mint").find(
                "span", class_="unit")
            try:
                factor = 1 if temp_item.contents[0].contents[0] == "+" else -1
            except IndexError:
                factor = 1
            temp = (temp + factor * int(temp_item.contents[1])) / 2

            # Просчитываем дату
            splitted_date = date.split()
            try:
                new_month = get_month_by_str(splitted_date[1])
                if current_month and current_month[1] == 12 and new_month[1] == 1:
                    current_year = current_year + 1
                current_month = new_month
            except IndexError:
                pass
            day_str = splitted_date[0]
            day_str = f"0{day_str}" if int(day_str) < 10 else day_str
            month_str = current_month[2]
            full_date = f"{current_year}-{month_str}-{day_str}"

            data.append({"date": full_date, "temp": temp})  # Заносим словарь в список

        return data

# Точка входа
def main():
    # Собираем информацию о погоде
    logger.info("Parsing: Weather")
    weather_by_date = {}
    for region in REGIONS:
        # logger.info("Collecting {} diary weather".format(region[0]))
        # diary_weather = get_gismeteio_diary(region[2], (2023, 5), (2023, 8))
        # for weather in diary_weather:
        #     if not (weather['date'] in weather_by_date):
        #         weather_by_date[weather['date']] = {}
        #     weather_by_date[weather['date']][region[0]] = weather['temp']
        
        # Получаем погоду региона на месяц и заносим данные в словарь
        logger.info("Collecting {} month weather".format(region[0]))
        month_weather = get_gismeteo_month(region[1])                       # Получаем погоду региона на месяц
        for weather in month_weather:                                       # Итерируем каждый день месяца
            if not (weather['date'] in weather_by_date):
                # Если даты нет в словаре - добавляем
                weather_by_date[weather['date']] = {}
            weather_by_date[weather['date']][region[0]] = weather['temp']   # Записываем данные о температуре для региона на дату
    
    # Заносим данные в БД
    logger.info("Commiting")
    session = Session()                                                             # Инициализация сессии БД
    for date in weather_by_date:
        china_weather = session.query(ChinaWeather).filter_by(date=date).first()    # Ищем в БД запись по дате
        
        # Если запись в БД не существует, создаем и добавляем ее
        if not china_weather:
            china_weather = ChinaWeather(date)
            session.add(china_weather)
            
        # Заносим данные в сущность
        china_weather.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        china_weather.beijing_temp = weather_by_date[date]['Beijing']
        china_weather.guangzhou_temp = weather_by_date[date]['Guangzhou']
        china_weather.shanghai_temp = weather_by_date[date]['Shanghai']
        china_weather.nanjing_temp = weather_by_date[date]['Nanjing']
        china_weather.calculate_average_temp()  # Просчитываем среднюю температуру по Китаю

        session.commit()    # Записываем данные в БД
    
    session.close()         # Закрываем сессию БД
    logger.info("Done!")


# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()
