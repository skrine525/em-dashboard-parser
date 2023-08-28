# Dashboard Parser

## Требования

Убедитесь, что у вас установлены следующие компоненты:

- Операционная система: Debian/Ubuntu
- Python: версия 3.8 и выше
- MySQL: установленный и настроенный сервер MySQL

## Установка

1. Клонируйте этот репозиторий на вашем компьютере:

   ```bash
   git clone https://github.com/skrine525/em-dashboard-parser
   ```
   
2. Перейдите в папку проекта:
    ```bash
    cd dashboard-parser
    ```
    
3. Установите необходимые зависимости, предпочтительно в виртуальной среде:
    ```bash
    pip3 install -r requirements.txt
    ```

4. Переименуйте файл **_config**.json в **config.json** и настройте его:
    ```json
    {
        "FILES_DIR": "Путь к папке с файлами для парсинга",
        "SQL_HOST": "Хост MySQL сервера",
        "SQL_USERNAME": "Пользователь MySQL",
        "SQL_PASSWORD": "Пароль MySQL",
        "SQL_DATABASE": "Имя БД"
    }
    ```

5. Выполните создание схемы БД:
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