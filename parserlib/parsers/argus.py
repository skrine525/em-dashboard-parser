import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from parserlib import config


# Константы
WAIT_TIMEOUT = 60
ENTRY_URL = "https://myaccount.argusmedia.com/login?ReturnUrl=https:%2F%2Fdirect.argusmedia.com%2Fdataanddownloads"
USERNAME_INPUT_XPATH = "/html/body/app-root/app-public/div[2]/div/app-login/div/div/form/div[1]/div/div[1]/input"
PASSWORD_INPUT_XPATH = "/html/body/app-root/app-public/div[2]/div/app-login/div/div/form/div[1]/div/div[2]/input"
SIGNIN_BUTTON_XPATH = "/html/body/app-root/app-public/div[2]/div/app-login/div/div/form/div[2]/div/button"
IFRAME_XPATH = "/html/body/app-root/app-layout/app-direct-frame/app-frame/iframe"
SECTOR_COAL_BUTTON_XPATH = "/html/body/div/div/div/div/div[1]/section/div[4]/div/div[2]/ul/li[1]"

# Инициализация драйвера
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, WAIT_TIMEOUT)

# Загрузка страницы входа
driver.get(ENTRY_URL)

# Производим вход в аккаунт
username_input = wait.until(EC.presence_of_element_located((By.XPATH, USERNAME_INPUT_XPATH)))
password_input = wait.until(EC.presence_of_element_located((By.XPATH, PASSWORD_INPUT_XPATH)))
signin_button = wait.until(EC.element_to_be_clickable((By.XPATH, SIGNIN_BUTTON_XPATH)))
username_input.send_keys(config.ARGUS_USERNAME)
password_input.send_keys(config.ARGUS_PASSWORD)
signin_button.click()

# Выбираем нужны сектор
# wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, IFRAME_XPATH)))
# sector_coal_button = wait.until(EC.visibility_of_element_located((By.XPATH, SECTOR_COAL_BUTTON_XPATH)))
# sector_coal_button.click()

time.sleep(100)