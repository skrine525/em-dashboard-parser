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
2. Клонируйте этот репозиторий на вашем компьютере:

   ```bash
   git clone https://github.com/skrine525/em-dashboard-parser
   ```
   
3. Перейдите в папку проекта:
    ```bash
    cd em-dashboard-parser
    ```
    
4. Установите необходимые зависимости, предпочтительно в виртуальной среде:
    ```bash
    pip3 install -r requirements.txt
    ```

5. Переименуйте файл **_config**.json в **config.json** и настройте его:
    ```json
    {
        "FILES_DIR": "Путь к папке с файлами для парсинга",
        "SQL_HOST": "Хост MySQL сервера",
        "SQL_USERNAME": "Пользователь MySQL",
        "SQL_PASSWORD": "Пароль MySQL",
        "SQL_DATABASE": "Имя БД"
    }
    ```

6. Выполните создание схемы БД:
    ```bash
    python3.8 initdb.py
    ```
    
## Запуск
Существует 4 режима запуска парсера:
- Парсинг погоды на месяц (Gismeteo):
    ```bash
    python3.8 parse.py gismeteo
    ```
- Парсинг фьючерсов (barchart.com и cmegroup.com):
    ```bash
    python3.8 parse.py features
    ```
- Парсинг PDF файлов из **%FILES_DIR%/pdf_cci** и **%FILES_DIR%/pdf_freight**:
    ```bash
    python3.8 parse.py pdf
    ```
- Парсинг XLS файлов из **%FILES_DIR%/xls_fob_vostochny** и **%FILES_DIR%/xls_ici3**:
    ```bash
    python3.8 parse.py xls
    ```