import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from parserlib.config import ARGUS_USERNAME, ARGUS_PASSWORD
from parserlib.paths import downloading_dir, freight_dir, ici3_dir, vostochny_dir
from parserlib.logger import logger


# Константы
WAIT_TIMEOUT = 60
ENTRY_URL = "https://myaccount.argusmedia.com/login?ReturnUrl=https:%2F%2Fdirect.argusmedia.com%2F"
PRICEDATA_URL = "https://direct.argusmedia.com/price/pricedata"
USERNAME_INPUT_XPATH = "/html/body/app-root/app-public/div[2]/div/app-login/div/div/form/div[1]/div/div[1]/input"
PASSWORD_INPUT_XPATH = "/html/body/app-root/app-public/div[2]/div/app-login/div/div/form/div[1]/div/div[2]/input"
SIGNIN_BUTTON_XPATH = "/html/body/app-root/app-public/div[2]/div/app-login/div/div/form/div[2]/div/button"
NAVMENU_PUBLICATIONS_XPATH = "/html/body/app-root/app-layout/navbar-menu/nav/div/div[1]/div[7]"
NAVMENU_PUBLICATIONS_DRYFREIGHT_PDF_XPATH = "/html/body/div[@class='ng-trigger ng-trigger-overlayAnimation ng-tns-c48-9 menu-scrollable p-menu p-component p-menu-overlay ng-star-inserted']/ul[@class='p-menu-list p-reset ng-tns-c48-9']/li[@class='p-element p-menuitem ng-tns-c48-9 publication-item ng-star-inserted'][1]/a[@id='ScrollableGroup']/span[@class='p-menuitem-text ng-star-inserted']/a[@id='pdf-link']"
PRICEDATA_IFRAME_XPATH = "/html/body/app-root/app-layout/app-direct-frame/app-frame/iframe"
ICI3_CHECKBOX_XPATH = "//*[@id='myPrices-42530000-4']/td[1]/input"
VOSTOCHNY_CHECKBOX_XPATH = "//*[@id='myPrices-202040600-8']/td[1]/input"
EXPORT_TO_EXCEL_BUTTON_XPATH = "//*[@id='price-data']/div/ul/li[3]/a"
EXPORT_PRICES_BUTTON_XPATH = "//*[@id='exportPriceSeriesButton']"
HOMEPAGE_IFRAME_XPATH = "/html/body/app-root/app-layout/app-direct-frame/app-frame/iframe"

# Настройки драйвера
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': downloading_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': False
})


# Загружает страницу аргуса, производит вход в аккаунт и возвращает кортеж, состоящий из веб-драйвера и wait-объекта
def signin() -> tuple:
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    # Загрузка страницы входа
    logger.info("Starting web driver")
    driver.get(ENTRY_URL)

    # Производим вход в аккаунт
    logger.info("Making an Argus account sign in")
    username_input = wait.until(EC.presence_of_element_located((By.XPATH, USERNAME_INPUT_XPATH)))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH)))
    signin_button = wait.until(EC.element_to_be_clickable((By.XPATH, SIGNIN_BUTTON_XPATH)))
    username_input.send_keys(ARGUS_USERNAME)
    password_input.send_keys(ARGUS_PASSWORD)
    signin_button.click()
    
    # Возвращаем кортеж
    return (driver, wait)


# Производит загрузку последнего файла фрахта
def download_freight_file(driver: webdriver.Chrome, wait: WebDriverWait):
    logger.info("Download: Freight file")
    
    # Очищаем папку загрузок
    logger.info("Cleaning up the download directory")
    for filename in os.listdir(downloading_dir):
        filepath = os.path.join(downloading_dir, filename)
        os.remove(filepath)
    
    # Переключаемся на стандартный контент
    driver.switch_to.default_content()
    
    # ИСПРАВЛЕНИЕ NAV-MENU ЛАГА:
    # Ждем пока появится iframe, переключаемся на него, и тут же переключаемся на стандартный контент
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, HOMEPAGE_IFRAME_XPATH)))
    driver.switch_to.default_content()
        
    # Производим загрузку файла
    logger.info("Downloading file")
    navmenu = wait.until(EC.presence_of_element_located((By.XPATH, NAVMENU_PUBLICATIONS_XPATH)))
    navmenu.click()
    pdf_button = wait.until(EC.presence_of_element_located((By.XPATH, NAVMENU_PUBLICATIONS_DRYFREIGHT_PDF_XPATH)))
    pdf_button.click()
    
    # Проивзодим поиск загруженного файла по расширению
    target_filename = None
    while True:
        for filename in os.listdir(downloading_dir):
            if filename.endswith("pdf"):
                target_filename = filename
                break
        
        # Если файл найден - выходим из цикла, иначе - делаем задержку в одну секунду
        if target_filename:
            break
        else:
            time.sleep(1)
    target_filepath = os.path.join(downloading_dir, target_filename)
    logger.info(f"File '{target_filename}' downloaded")
    
    # Получаем дату из названия файла
    i = target_filename.find("(") + 1
    j = target_filename.find(")", i)
    date = target_filename[i:j].replace("-", "")
    
    # Переименовываем файл и отправляем в директорию для парсинга
    fixed_filename = f"{date}_Argus_Freight.pdf"
    fixed_filepath = os.path.join(freight_dir, fixed_filename)
    if os.path.exists(fixed_filepath):
        logger.info(f"File '{fixed_filepath}' already exists")
    else:
        os.rename(target_filepath, fixed_filepath)
        logger.info(f"File '{fixed_filename}' moved to '{freight_dir}'")
    
    logger.info("Done!")
        
# Производит загрузку последнего файла ICI3
def download_ici3_file(driver: webdriver.Chrome, wait: WebDriverWait):
    logger.info("Download: ICI3 file")
    
    # Очищаем папку загрузок
    logger.info("Cleaning up the download directory")
    for filename in os.listdir(downloading_dir):
        filepath = os.path.join(downloading_dir, filename)
        os.remove(filepath)
    
    # Переходим на страницу с ценовыми данными
    logger.info("Going to the page with price data")
    driver.get(PRICEDATA_URL)
    
    # Переключаемся на стандартный контент
    driver.switch_to.default_content()
    
    # Выбираем нужный файл и производим загрузку
    logger.info("Downloading file")
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, PRICEDATA_IFRAME_XPATH)))
    checkbox = wait.until(EC.visibility_of_element_located((By.XPATH, ICI3_CHECKBOX_XPATH)))
    checkbox.click()
    export_to_excel_button = wait.until(EC.visibility_of_element_located((By.XPATH, EXPORT_TO_EXCEL_BUTTON_XPATH)))
    export_to_excel_button.click()
    export_prices_button = wait.until(EC.visibility_of_element_located((By.XPATH, EXPORT_PRICES_BUTTON_XPATH)))
    export_prices_button.click()
    
    # Проивзодим поиск загруженного файла по расширению
    target_filename = None
    while True:
        for filename in os.listdir(downloading_dir):
            if filename.endswith("xls"):
                target_filename = filename
                break
        
        # Если файл найден - выходим из цикла, иначе - делаем задержку в одну секунду
        if target_filename:
            break
        else:
            time.sleep(1)
    target_filepath = os.path.join(downloading_dir, target_filename)
    logger.info(f"File '{target_filename}' downloaded")
    
    # Получаем дату из названия файла
    i = target_filename.find("(") + 1
    j = target_filename.find(")", i)
    date = target_filename[i:j]
    
    # Переименовываем файл и отправляем в директорию для парсинга
    fixed_filename = f"ICI3 ({date}).xls"
    fixed_filepath = os.path.join(ici3_dir, fixed_filename)
    if os.path.exists(fixed_filepath):
        logger.info(f"File '{fixed_filepath}' already exists")
    else:
        os.rename(target_filepath, fixed_filepath)
        logger.info(f"File '{fixed_filename}' moved to '{ici3_dir}'")
        
    logger.info("Done!")
    
# Производит загрузку последнего файла FOB Vostochny
def download_vostochny_file(driver: webdriver.Chrome, wait: WebDriverWait):
    logger.info("Download: FOB Vostochny file")
    
    # Очищаем папку загрузок
    logger.info("Cleaning up the download directory")
    for filename in os.listdir(downloading_dir):
        filepath = os.path.join(downloading_dir, filename)
        os.remove(filepath)
    
    # Переходим на страницу с ценовыми данными
    logger.info("Going to the page with price data")
    driver.get(PRICEDATA_URL)
    
    # Переключаемся на стандартный контент
    driver.switch_to.default_content()
    
    # Выбираем нужный файл и производим загрузку
    logger.info("Downloading file")
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, PRICEDATA_IFRAME_XPATH)))
    checkbox = wait.until(EC.visibility_of_element_located((By.XPATH, VOSTOCHNY_CHECKBOX_XPATH)))
    checkbox.click()
    export_to_excel_button = wait.until(EC.visibility_of_element_located((By.XPATH, EXPORT_TO_EXCEL_BUTTON_XPATH)))
    export_to_excel_button.click()
    export_prices_button = wait.until(EC.visibility_of_element_located((By.XPATH, EXPORT_PRICES_BUTTON_XPATH)))
    export_prices_button.click()
    
    # Проивзодим поиск загруженного файла по расширению
    target_filename = None
    while True:
        for filename in os.listdir(downloading_dir):
            if filename.endswith("xls"):
                target_filename = filename
                break
        
        # Если файл найден - выходим из цикла, иначе - делаем задержку в одну секунду
        if target_filename:
            break
        else:
            time.sleep(1)
    target_filepath = os.path.join(downloading_dir, target_filename)
    logger.info(f"File '{target_filename}' downloaded")
    
    # Получаем дату из названия файла
    i = target_filename.find("(") + 1
    j = target_filename.find(")", i)
    date = target_filename[i:j]
    
    # Переименовываем файл и отправляем в директорию для парсинга
    fixed_filename = f"FOB Vostochny ({date}).xls"
    fixed_filepath = os.path.join(vostochny_dir, fixed_filename)
    if os.path.exists(fixed_filepath):
        logger.info(f"File '{fixed_filepath}' already exists")
    else:
        os.rename(target_filepath, fixed_filepath)
        logger.info(f"File '{fixed_filename}' moved to '{vostochny_dir}'")
        
    logger.info("Done!")

# Точка входа
def main():
    logger.info("Starting Argus downloading")
    driver, wait = signin()
    download_freight_file(driver, wait)
    download_ici3_file(driver, wait)
    download_vostochny_file(driver, wait)
    driver.quit()

# Если файл был запущен, а не импортирован
if __name__ == "__main__":
    main()
