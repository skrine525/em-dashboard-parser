# Dashboard Parser

## Требования

Убедитесь, что у вас установлены следующие компоненты:

- Операционная система: Debian/Ubuntu
- Python: версия 3.8 и выше
- MySQL: установленный и настроенный сервер MySQL

## Установка
1. Установите браузер Chrome:
    ```bash
    wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
    sudo apt update
    sudo apt install -f ./google-chrome-stable_current_amd64.deb 
    ```

2. Установите Tesseract OCR
    ```bash
    sudo apt install tesseract-ocr
    sudo apt install libtesseract-dev
    ```
3. Клонируйте этот репозиторий на вашем компьютере:

   ```bash
   git clone https://github.com/skrine525/em-dashboard-parser
   ```
   
4. Перейдите в папку проекта:
    ```bash
    cd em-dashboard-parser
    ```
    
5. Установите необходимые зависимости, предпочтительно в виртуальной среде:
    ```bash
    pip3 install -r requirements.txt
    ```

6. Переименуйте файл **_config.json** в **config.json** и настройте его:
    ```json
    {
        "FILES_DIR": "Путь к папке с файлами для парсинга",
        "SQL_HOST": "Хост MySQL сервера",
        "SQL_USERNAME": "Пользователь MySQL",
        "SQL_PASSWORD": "Пароль MySQL",
        "SQL_DATABASE": "Имя БД",
        "ARGUS_USERNAME": "Логин Argus Media",
        "ARGUS_PASSWORD": "Пароль Argus Media",
        "EMAIL_SERVER": "Exchange сервер почты",
        "EMAIL_ADDRESS": "Адрес почты",
        "EMAIL_PASSWORD": "Пароль почты"
    }
    ```

7. Выполните создание схемы БД:
    ```bash
    python3.8 initdb.py
    ```

## Скачивание
Существует 3 режима скачивания
- Скачивание файлов из **Argus Media**:
    ```bash
    python3.8 download.py argus
    ```
- Скачивание файлов **CCI Daily** из почты:
    ```bash
    python3.8 parse.py cci
    ```
- Скачивание **"ручных" XLSX файлов** из почты:
    ```bash
    python3.8 parse.py manual-xlsx
    ```

## Парсинг
Существует 5 режима парсинга:
- Парсинг **погоды** на месяц (Gismeteo):
    ```bash
    python3.8 parse.py gismeteo
    ```
- Парсинг **фьючерсов** (barchart.com и cmegroup.com):
    ```bash
    python3.8 parse.py futures
    ```
- Парсинг **PDF файлов** из **%FILES_DIR%/pdf_cci** и **%FILES_DIR%/pdf_freight**:
    ```bash
    python3.8 parse.py pdf
    ```
- Парсинг **XLS файлов** из **%FILES_DIR%/xls_fob_vostochny** и **%FILES_DIR%/xls_ici3**:
    ```bash
    python3.8 parse.py xls
    ```
- Парсинг **"ручного" XLSX файла**
    ```bash
    python3.8 parse.py manual-xlsx
    ```