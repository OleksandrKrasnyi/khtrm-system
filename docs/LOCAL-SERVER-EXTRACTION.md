# Извлечение данных с локального сервера

## 📋 Обзор

Поскольку SSH недоступен, создан скрипт для запуска непосредственно на Windows сервере. Этот скрипт найдет все MS Access файлы, проверит MySQL подключение и создаст отчет.

## 🎯 Цель

Получить полную информацию о данных на сервере для разработки функционала нарядчика.

## 📁 Файлы для копирования на сервер

1. **`scripts/local_server_extraction.py`** - основной скрипт
2. **`scripts/requirements.txt`** - зависимости (опционально)

## 🚀 Инструкция по запуску

### Шаг 1: Подготовка на сервере

```bash
# Создать папку для скрипта
mkdir C:\DataExtraction
cd C:\DataExtraction

# Скопировать файл local_server_extraction.py в эту папку
```

### Шаг 2: Установка Python (если не установлен)

```bash
# Скачать Python с https://www.python.org/downloads/
# Установить с опцией "Add Python to PATH"

# Проверить установку
python --version
```

### Шаг 3: Запуск скрипта

```bash
# Запустить скрипт
python local_server_extraction.py

# Или использовать batch файл (создается автоматически)
run_extraction.bat
```

## 📊 Что скрипт делает

### 1. Системная информация
- Имя хоста
- Версия ОС
- Текущий пользователь
- Информация о дисках
- Запущенные процессы
- Сетевая конфигурация

### 2. Поиск MS Access файлов
- Ищет в стандартных папках:
  - `C:\`
  - `D:\`
  - `C:\Program Files\`
  - `C:\Users\`
  - `C:\Data\`
  - `C:\Transport\`
  - `C:\Depot\`
- Находит файлы: `.mdb`, `.accdb`, `.mde`, `.accde`
- Записывает размер и дату изменения

### 3. Тест MySQL подключения
- Проверяет разные варианты подключения:
  - `mysql -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'`
  - `mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'`
  - `mysql -h 127.0.0.1 -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'`
- Получает список таблиц из `saltdepoavt_`

### 4. Поиск файлов базы данных
- SQL файлы (*.sql, *.bak)
- Backup файлы (*.bak, *.backup)
- Конфигурационные файлы (*.ini, *.cfg, *.conf)
- Лог файлы (*.log, *.txt)

## 📄 Результаты

После выполнения создается папка `extraction_results` с файлами:

```
extraction_results/
├── local_extraction_20250115_143022.json    # Данные в JSON формате
├── local_extraction_report_20250115_143022.md # Читаемый отчет
└── run_extraction.bat                        # Batch файл для повторного запуска
```

## 📋 Пример результата

### MS Access файлы
```json
{
  "access_files": [
    {
      "path": "C:\\Transport\\Database\\depot.mdb",
      "size": 15728640,
      "modified": "2024-12-15T14:30:00"
    },
    {
      "path": "C:\\Data\\saltdepo.accdb", 
      "size": 8456320,
      "modified": "2025-01-10T09:15:00"
    }
  ]
}
```

### MySQL подключение
```json
{
  "mysql_info": {
    "connection_status": "success",
    "command_used": "mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'",
    "saltdepoavt_tables": "Tables_in_saltdepoavt_\\nzanaradka\\nsprmarshrut\\nsprpersonal\\nsprpe"
  }
}
```

## 📤 Передача результатов

После выполнения скрипта:

1. **Заархивировать папку `extraction_results`**
2. **Отправить архив команде разработки**
3. **Или скопировать файлы через общую папку/email**

## 🔧 Альтернативные методы

### Если Python недоступен

Создать простой batch файл для сбора базовой информации:

```batch
@echo off
echo Starting manual data collection...

echo System Information > system_info.txt
hostname >> system_info.txt
ver >> system_info.txt
whoami >> system_info.txt
ipconfig /all >> system_info.txt

echo Searching for Access files...
dir /s /b C:\*.mdb > access_files.txt
dir /s /b C:\*.accdb >> access_files.txt
dir /s /b D:\*.mdb >> access_files.txt
dir /s /b D:\*.accdb >> access_files.txt

echo Testing MySQL...
mysql -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;' > mysql_test.txt
mysql -h localhost -u khtrm_remote -p'KhTRM_2025!' saltdepoavt_ -e 'SHOW TABLES;' > mysql_tables.txt

echo Done! Check the generated .txt files
pause
```

## 🚨 Безопасность

- Скрипт содержит пароли в открытом виде
- Используйте только для разработки
- Удалите скрипт после использования
- Не передавайте пароли в незащищенном виде

## 🔍 Отладка

### Если скрипт не запускается
```bash
# Проверить Python
python --version

# Запустить с отладкой
python -u local_server_extraction.py

# Проверить права доступа
# Запустить как администратор
```

### Если MySQL не подключается
```bash
# Проверить вручную
mysql -u khtrm_remote -p'KhTRM_2025!' -e 'SHOW DATABASES;'

# Проверить службы
services.msc
# Найти MySQL и проверить статус
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте права доступа к папкам
2. Убедитесь, что MySQL запущен
3. Проверьте пароли и имена пользователей
4. Запустите скрипт от имени администратора
5. Отправьте файлы логов разработчикам 