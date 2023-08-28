import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from parserlib.db.model import Future
from parserlib.db.engine import Session
from parserlib.logger import logger


# Константы
URL_COAL = "https://www.barchart.com/futures/quotes/LQ*0/futures-prices"
URL_GAS = "https://www.cmegroup.com/markets/energy/natural-gas/dutch-ttf-natural-gas-financial-usd-mmbtu-icis-heren-m1-average-price-calendar-month.html#venue=globex"
WAIT_TIMEOUT = 60
MONTHS = [
    ['jan', 1, '01'],
    ['feb', 2, '02'],
    ['mar', 3, '03'],
    ['apr', 4, '04'],
    ['may', 5, '05'],
    ['jun', 6, '06'],
    ['jul', 7, '07'],
    ['aug', 8, '08'],
    ['sep', 9, '09'],
    ['oct', 10, '10'],
    ['nov', 11, '11'],
    ['dec', 12, '12'],
]

# Настройки драйвера
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Возвращает дату по месяцу контракта угля
def get_date_by_coal_contract_symbol(contract_symbol: str) -> int:
    # Парсим дату
    i = contract_symbol.find('(') + 1
    j = contract_symbol.find(')', i)
    parsed_date = contract_symbol[i:j]
    
    # Получаем строковый порядок месяца
    i = parsed_date.find(' ')
    parsed_month = parsed_date[:i].lower()
    month_str = ''
    for month in MONTHS:
        if month[0] == parsed_month:
            month_str = month[2]
            break
        
    # Парсим год
    j = i + 2
    year_str = parsed_date[j:]
    
    # Формируем дату
    date = f'20{year_str}-{month_str}-01'
    return date

# Возвращает дату по месяцу контракта газа
def get_date_by_gas_month(month: str) -> int:
    # Парсим месяц и год
    splitted_month = month.lower().split()
    
    # Получаем строковый порядок месяца
    month_str = ''
    for month in MONTHS:
        if month[0] == splitted_month[0]:
            month_str = month[2]
            break
    
    # Формируем дату
    date = f'{splitted_month[1]}-{month_str}-01'
    return date

# Парсит и записывает данные в БД по фьючерсам газа
def write_gas_features():
    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    
    # Загружаем страницу
    logger.info("Starting web driver")
    driver.get(URL_GAS)
    
    # Ждем, пока появится таблица
    logger.info("Waiting the table")
    tbody = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[3]/div[3]/div/div/div/div/div/div[2]/div/div/div/div/div/div[6]/div/div/div/div[1]/div/table/tbody')))
    
    # Парсим строки таблицы
    logger.info("Parsing the table")
    session = Session()                                     # Инициализация сессии БД
    tr_list = tbody.find_elements(By.TAG_NAME, 'tr')        # Получаем список строк таблицы
    count = 0                                               # Количество спарсенных строк
    for tr in tr_list:
        td_list = tr.find_elements(By.TAG_NAME, 'td')       # Парсим столбцы строки
        
        date_td = td_list[0]                                # Получаем элемент даты
        prior_settle_td = td_list[4]                        # Получаем элемент данных
        
        month = date_td.find_element(By.TAG_NAME, "b").get_attribute('innerHTML')       # Парсим дату
        prior_settle = float(prior_settle_td.find_element(By.TAG_NAME, 'div').text)     # Парсим данные
        
        date = get_date_by_gas_month(month)                             # Преобразуем дату в YYYY-MM-DD
        future = session.query(Future).filter_by(date=date).first()     # Ищем в БД запись по дате
        
        # Если запись в БД не существует, создаем и добавляем ее
        if not future:
            future = Future(date)
            session.add(future)
        
        # Заносим данные в сущность
        future.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        future.gas_prior_settle = prior_settle
        
        session.commit()        # Записываем данные в БД
        
        # Парсим только первые 12 строк
        count = count + 1
        if count >= 12:
            break
    
    driver.quit()               # Закрываем веб драйвер
    session.close()             # Закрываем сессию БД
    logger.info("Done!")

# Парсит и записывает данные в БД по фьючерсам угля
def write_coal_features():
    # Инициализация драйвера
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    
    # Загружаем страницу
    logger.info("Starting web driver")
    driver.get(URL_COAL)
    
    # Ждем пока появится сетка с данным
    logger.info("Waiting the grid")
    shadow_host = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div[5]/div/div[2]/bc-data-grid')))
    
    # Парсим сетку с данными
    logger.info("Parsing the grid")
    grid_shadow_root = shadow_host.shadow_root
    grid = grid_shadow_root.find_element(By.ID, '_grid')
    rows = grid.find_elements(By.CLASS_NAME, 'row')
    
    # Парсим строки сетки
    logger.info("Parsing rows")
    session = Session()             # Инициализация сессии БД
    count = 0                       # Количество спарсенных строк
    for row in rows:
        # Получаем shadow-root первого и второго столбца
        contract_symbol = row.find_element(By.CLASS_NAME, 'contractSymbol').find_element(By.TAG_NAME, 'text-binding')
        last_price = row.find_element(By.CLASS_NAME, 'lastPrice').find_element(By.TAG_NAME, 'text-binding')
        
        # Достаем данные из shadow-root
        contract_symbol_text = driver.execute_script('return arguments[0].shadowRoot.textContent', contract_symbol)
        last_price_text = driver.execute_script('return arguments[0].shadowRoot.textContent', last_price)
        
        date = get_date_by_coal_contract_symbol(contract_symbol_text)   # Преобразуем дату в YYYY-MM-DD
        last_price_value = float(last_price_text.replace("s", ''))      # Преобразуем цену в число
        future = session.query(Future).filter_by(date=date).first()     # Ищем в БД запись по дате
        
        # Если запись в БД не существует, создаем и добавляем ее
        if not future:
            future = Future(date)
            session.add(future)
        
        # Заносим данные в сущность
        future.update_timestamp = int(datetime.datetime.utcnow().timestamp())
        future.coal_last_price = last_price_value
        
        session.commit()    # Записываем данные в БД
        
        # Парсим только первые 12 строк
        count = count + 1
        if count >= 12:
            break
    
    driver.quit()               # Закрываем веб драйвер
    session.close()             # Закрываем сессию БД
    logger.info("Done!")

# Точка входа
def main():
    # Запускаем парсинг фьючерсов угля
    logger.info("Parsing: Coal features")
    write_coal_features()
    
    # Запускаем парсинг фьючерсов газа
    logger.info("Parsing: Gas features")
    write_gas_features()
    

# Если файл был запущен, а не импортирован
if __name__ == '__main__':
    main()
