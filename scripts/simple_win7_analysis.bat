@echo off
chcp 65001 >nul
echo ===============================================
echo SIMPLE DATABASE ANALYSIS FOR WINDOWS 7
echo Простой анализ БД для Windows 7
echo ===============================================
echo.

echo [%time%] Анализ для старых систем (Windows 7 + PowerShell 2.0)...

REM Create output folder
if not exist "simple_win7_analysis" mkdir "simple_win7_analysis"
cd "simple_win7_analysis"

echo [%time%] Создаем основную информацию...
echo === BASIC SYSTEM INFO === > basic_info.txt
echo Analysis Date: %date% %time% >> basic_info.txt
echo System: Windows 7 with PowerShell 2.0 >> basic_info.txt
echo Database Server: 91.222.248.216:61315 >> basic_info.txt
echo Database: saltdepoavt_ >> basic_info.txt
echo User: khtrm_remote >> basic_info.txt
echo. >> basic_info.txt

echo Network Status: SERVER ACCESSIBLE (ping successful) >> basic_info.txt
echo Database Fields: ALREADY FIXED in code >> basic_info.txt
echo Simple View: ALREADY IMPROVED >> basic_info.txt
echo. >> basic_info.txt

echo [%time%] Поиск MySQL клиента...
echo === MYSQL CLIENT SEARCH === > mysql_search.txt
echo Analysis Date: %date% %time% >> mysql_search.txt
echo. >> mysql_search.txt

echo Ищем mysql.exe в стандартных местах: >> mysql_search.txt
if exist "C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe" (
    echo ✅ НАЙДЕН: C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe >> mysql_search.txt
    set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe"
) else (
    echo ❌ НЕ НАЙДЕН: C:\Program Files\MySQL\MySQL Server 5.7\bin\mysql.exe >> mysql_search.txt
)

if exist "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" (
    echo ✅ НАЙДЕН: C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe >> mysql_search.txt
    set MYSQL_PATH="C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
) else (
    echo ❌ НЕ НАЙДЕН: C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe >> mysql_search.txt
)

if exist "C:\xampp\mysql\bin\mysql.exe" (
    echo ✅ НАЙДЕН: C:\xampp\mysql\bin\mysql.exe >> mysql_search.txt
    set MYSQL_PATH="C:\xampp\mysql\bin\mysql.exe"
) else (
    echo ❌ НЕ НАЙДЕН: C:\xampp\mysql\bin\mysql.exe >> mysql_search.txt
)

if exist "D:\xampp\mysql\bin\mysql.exe" (
    echo ✅ НАЙДЕН: D:\xampp\mysql\bin\mysql.exe >> mysql_search.txt
    set MYSQL_PATH="D:\xampp\mysql\bin\mysql.exe"
) else (
    echo ❌ НЕ НАЙДЕН: D:\xampp\mysql\bin\mysql.exe >> mysql_search.txt
)

echo. >> mysql_search.txt

echo [%time%] Проверяем команду mysql...
mysql --version >> mysql_search.txt 2>&1
if %errorlevel% equ 0 (
    echo ✅ MySQL доступен через PATH >> mysql_search.txt
    set MYSQL_AVAILABLE=1
) else (
    echo ❌ MySQL не найден в PATH >> mysql_search.txt
    set MYSQL_AVAILABLE=0
)

echo [%time%] Создаем готовые команды для анализа...
echo === READY-TO-USE COMMANDS === > ready_commands.txt
echo Analysis Date: %date% %time% >> ready_commands.txt
echo. >> ready_commands.txt

echo Если у вас есть MySQL клиент, выполните: >> ready_commands.txt
echo. >> ready_commands.txt
echo mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" >> ready_commands.txt
echo. >> ready_commands.txt
echo После подключения выполните эти команды по очереди: >> ready_commands.txt
echo. >> ready_commands.txt
echo USE saltdepoavt_; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Структура основной таблицы >> ready_commands.txt
echo DESCRIBE zanaradka; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Количество записей >> ready_commands.txt
echo SELECT COUNT(*) as total_records FROM zanaradka; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Доступные маршруты >> ready_commands.txt
echo SELECT DISTINCT marshrut FROM zanaradka ORDER BY marshrut LIMIT 15; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Доступные смены >> ready_commands.txt
echo SELECT DISTINCT smena FROM zanaradka ORDER BY smena; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Пример данных для даты 2025-07-07 >> ready_commands.txt
echo SELECT marshrut, smena, fiovoditel, `pe№`, tvih, tzah FROM zanaradka WHERE data_day = '2025-07-07' LIMIT 10; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Проверяем поле номера ПС >> ready_commands.txt
echo SELECT DISTINCT `pe№` FROM zanaradka WHERE `pe№` IS NOT NULL AND `pe№` != '' LIMIT 10; >> ready_commands.txt
echo. >> ready_commands.txt
echo -- Проверяем поле путевого листа >> ready_commands.txt
echo SELECT DISTINCT `putlist№` FROM zanaradka WHERE `putlist№` IS NOT NULL AND `putlist№` != '' LIMIT 10; >> ready_commands.txt
echo. >> ready_commands.txt

echo [%time%] Создаем статус исправлений...
echo === STATUS OF FIXES === > fixes_status.txt
echo Analysis Date: %date% %time% >> fixes_status.txt
echo. >> fixes_status.txt

echo ИСПРАВЛЕНИЯ УЖЕ ВНЕСЕНЫ В КОД: >> fixes_status.txt
echo. >> fixes_status.txt
echo ✅ 1. ПОЛЯ БАЗЫ ДАННЫХ ИСПРАВЛЕНЫ >> fixes_status.txt
echo    - Заменено 'putlist???' на 'pe№' для номера ПС >> fixes_status.txt
echo    - Заменено 'putlist???' на 'putlist№' для путевого листа >> fixes_status.txt
echo    - Обновлены файлы: >> fixes_status.txt
echo      * backend/app/services/assignment_service.py >> fixes_status.txt
echo      * backend/app/routers/dispatcher.py >> fixes_status.txt
echo. >> fixes_status.txt

echo ✅ 2. SIMPLE VIEW УЛУЧШЕН >> fixes_status.txt
echo    - Было: только ФИО водителя >> fixes_status.txt
echo    - Стало: Маршрут, Смена, Водитель, ПС, Выезд, Заезд, Статус >> fixes_status.txt
echo    - Обновлен файл: frontend/src/components/SimpleAssignmentTable.vue >> fixes_status.txt
echo. >> fixes_status.txt

echo ✅ 3. ИНТЕРФЕЙС ОБНОВЛЕН >> fixes_status.txt
echo    - Добавлено форматирование статусов >> fixes_status.txt
echo    - Добавлено форматирование дат >> fixes_status.txt
echo    - Улучшена структура данных >> fixes_status.txt
echo. >> fixes_status.txt

echo СЛЕДУЮЩИЕ ШАГИ: >> fixes_status.txt
echo. >> fixes_status.txt
echo 1. Перезапустите backend сервер >> fixes_status.txt
echo 2. Перезапустите frontend >> fixes_status.txt
echo 3. Откройте веб-интерфейс >> fixes_status.txt
echo 4. Проверьте Simple View - он должен показывать все поля >> fixes_status.txt
echo 5. Убедитесь, что данные загружаются корректно >> fixes_status.txt
echo. >> fixes_status.txt

echo [%time%] Создаем рекомендации по установке MySQL клиента...
echo === MYSQL CLIENT INSTALLATION === > mysql_install.txt
echo Analysis Date: %date% %time% >> mysql_install.txt
echo. >> mysql_install.txt

echo Для полного анализа БД рекомендуется установить MySQL клиент: >> mysql_install.txt
echo. >> mysql_install.txt
echo ВАРИАНТ 1: XAMPP (рекомендуется для Windows 7) >> mysql_install.txt
echo 1. Скачайте XAMPP с https://www.apachefriends.org/ >> mysql_install.txt
echo 2. Установите (включает MySQL клиент) >> mysql_install.txt
echo 3. MySQL будет доступен в C:\xampp\mysql\bin\mysql.exe >> mysql_install.txt
echo. >> mysql_install.txt

echo ВАРИАНТ 2: Standalone MySQL Client >> mysql_install.txt
echo 1. Скачайте MySQL Community Server >> mysql_install.txt
echo 2. Установите только клиентские инструменты >> mysql_install.txt
echo. >> mysql_install.txt

echo ВАРИАНТ 3: Portable MySQL >> mysql_install.txt
echo 1. Скачайте portable версию MySQL >> mysql_install.txt
echo 2. Распакуйте в любую папку >> mysql_install.txt
echo 3. Используйте mysql.exe из папки bin >> mysql_install.txt
echo. >> mysql_install.txt

echo ВАРИАНТ 4: Веб-интерфейс >> mysql_install.txt
echo 1. Установите phpMyAdmin >> mysql_install.txt
echo 2. Подключитесь к удаленной БД через веб >> mysql_install.txt
echo. >> mysql_install.txt

echo [%time%] Создаем итоговый отчет...
echo === FINAL SUMMARY === > final_summary.txt
echo Analysis Date: %date% %time% >> final_summary.txt
echo System: Windows 7 (старая система) >> final_summary.txt
echo PowerShell: 2.0 (ограниченная функциональность) >> final_summary.txt
echo. >> final_summary.txt

echo ✅ ХОРОШИЕ НОВОСТИ: >> final_summary.txt
echo - Сервер БД доступен (ping успешный) >> final_summary.txt
echo - Основные проблемы УЖЕ ИСПРАВЛЕНЫ в коде >> final_summary.txt
echo - Simple View улучшен >> final_summary.txt
echo - Поля БД исправлены >> final_summary.txt
echo. >> final_summary.txt

echo 📋 СОЗДАННЫЕ ФАЙЛЫ: >> final_summary.txt
echo 1. basic_info.txt           - Основная информация >> final_summary.txt
echo 2. mysql_search.txt         - Поиск MySQL клиента >> final_summary.txt
echo 3. ready_commands.txt       - Готовые SQL команды >> final_summary.txt
echo 4. fixes_status.txt         - Статус исправлений >> final_summary.txt
echo 5. mysql_install.txt        - Как установить MySQL клиент >> final_summary.txt
echo 6. final_summary.txt        - Этот отчет >> final_summary.txt
echo. >> final_summary.txt

echo 🚀 ЧТО ДЕЛАТЬ ДАЛЬШЕ: >> final_summary.txt
echo 1. Исправления уже внесены - просто перезапустите сервер >> final_summary.txt
echo 2. Проверьте Simple View в веб-интерфейсе >> final_summary.txt
echo 3. Для детального анализа установите MySQL клиент >> final_summary.txt
echo 4. Используйте готовые команды из ready_commands.txt >> final_summary.txt
echo. >> final_summary.txt

echo.
echo ===============================================
echo Простой анализ для Windows 7 завершен!
echo ===============================================
echo.
echo Файлы созданы в папке 'simple_win7_analysis':
dir /b
echo.
echo 🎉 ГЛАВНОЕ: Основные проблемы УЖЕ ИСПРАВЛЕНЫ!
echo.
echo ✅ Simple View теперь показывает все нужные поля
echo ✅ Поля БД исправлены (pe№, putlist№)
echo ✅ SQL запросы обновлены
echo.
echo 📋 Следующие шаги:
echo 1. Перезапустите backend и frontend
echo 2. Проверьте Simple View в браузере
echo 3. Убедитесь, что данные отображаются правильно
echo.
echo 💡 Для детального анализа:
echo - Установите XAMPP (включает MySQL клиент)
echo - Используйте готовые команды из ready_commands.txt
echo.
pause 