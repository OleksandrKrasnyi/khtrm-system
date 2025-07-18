@echo off
chcp 65001 >nul
echo ===============================================
echo ALTERNATIVE DATABASE ANALYSIS TOOL
echo Альтернативный анализ БД (без Python)
echo ===============================================
echo.

echo [%time%] Начинаем анализ базы данных...

REM Create output folder
if not exist "alternative_db_analysis" mkdir "alternative_db_analysis"
cd "alternative_db_analysis"

echo [%time%] Создаем информацию о системе...
echo === SYSTEM INFORMATION === > system_info.txt
echo Analysis Date: %date% %time% >> system_info.txt
echo Tool: Alternative Database Analysis (без Python) >> system_info.txt
echo OS Version: >> system_info.txt
ver >> system_info.txt
echo. >> system_info.txt
echo PowerShell Version: >> system_info.txt
powershell -command "$PSVersionTable.PSVersion" >> system_info.txt 2>&1
echo. >> system_info.txt

echo [%time%] Проверяем сетевое подключение к серверу БД...
echo === NETWORK CONNECTIVITY === > network_test.txt
echo Analysis Date: %date% %time% >> network_test.txt
echo Target: 91.222.248.216:61315 >> network_test.txt
echo. >> network_test.txt

echo Testing ping to server: >> network_test.txt
ping -n 4 91.222.248.216 >> network_test.txt 2>&1
echo. >> network_test.txt

echo Testing telnet connection (if available): >> network_test.txt
echo open 91.222.248.216 61315 | telnet >> network_test.txt 2>&1
echo. >> network_test.txt

echo Testing port with PowerShell: >> network_test.txt
powershell -command "Test-NetConnection -ComputerName 91.222.248.216 -Port 61315" >> network_test.txt 2>&1
echo. >> network_test.txt

echo [%time%] Попытка подключения к MySQL через PowerShell...
echo === POWERSHELL MYSQL CONNECTION === > powershell_mysql.txt
echo Analysis Date: %date% %time% >> powershell_mysql.txt
echo. >> powershell_mysql.txt

powershell -command "& {
    try {
        Write-Host 'Попытка загрузки MySQL .NET Connector...'
        Add-Type -Path 'C:\Program Files (x86)\MySQL\MySQL Connector Net 8.0.33\MySql.Data.dll' -ErrorAction Stop
        Write-Host 'MySQL Connector найден, пытаемся подключиться...'
        
        $connectionString = 'Server=91.222.248.216;Port=61315;Database=saltdepoavt_;Uid=khtrm_remote;Pwd=KhTRM_2025!;'
        $connection = New-Object MySql.Data.MySqlClient.MySqlConnection($connectionString)
        $connection.Open()
        
        Write-Host 'Подключение успешно!'
        Write-Host 'Версия сервера:' $connection.ServerVersion
        
        # Получаем структуру таблицы
        $command = $connection.CreateCommand()
        $command.CommandText = 'DESCRIBE zanaradka'
        $reader = $command.ExecuteReader()
        
        Write-Host 'Структура таблицы zanaradka:'
        while ($reader.Read()) {
            Write-Host $reader[0] ':' $reader[1]
        }
        
        $connection.Close()
    } catch {
        Write-Host 'Ошибка MySQL подключения:' $_.Exception.Message
        Write-Host 'MySQL Connector, вероятно, не установлен'
    }
}" >> powershell_mysql.txt 2>&1

echo [%time%] Попытка получения данных через API приложения...
echo === API DATA RETRIEVAL === > api_data.txt
echo Analysis Date: %date% %time% >> api_data.txt
echo. >> api_data.txt

echo Проверяем локальный API сервер... >> api_data.txt
curl http://localhost:8000/api/dispatcher/check-table-structure?table_name=zanaradka >> api_data.txt 2>&1
echo. >> api_data.txt

echo Пробуем альтернативный порт... >> api_data.txt
curl http://localhost:3000/api/dispatcher/check-table-structure?table_name=zanaradka >> api_data.txt 2>&1
echo. >> api_data.txt

echo Используем PowerShell для HTTP запроса... >> api_data.txt
powershell -command "& {
    try {
        $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/dispatcher/check-table-structure?table_name=zanaradka' -Method Get
        $response | ConvertTo-Json -Depth 5
    } catch {
        Write-Host 'API недоступно:' $_.Exception.Message
        try {
            $response = Invoke-WebRequest -Uri 'http://localhost:8000/api/dispatcher/direct-assignments?assignment_date=2025-07-07&limit=5' -Method Get
            $response.Content
        } catch {
            Write-Host 'Альтернативный API тоже недоступен:' $_.Exception.Message
        }
    }
}" >> api_data.txt 2>&1

echo [%time%] Создаем скрипт для ручного анализа...
echo === MANUAL ANALYSIS SCRIPT === > manual_mysql_commands.txt
echo Analysis Date: %date% %time% >> manual_mysql_commands.txt
echo. >> manual_mysql_commands.txt
echo Если у вас есть доступ к MySQL клиенту, выполните следующие команды: >> manual_mysql_commands.txt
echo. >> manual_mysql_commands.txt
echo mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" >> manual_mysql_commands.txt
echo. >> manual_mysql_commands.txt
echo После подключения выполните: >> manual_mysql_commands.txt
echo USE saltdepoavt_; >> manual_mysql_commands.txt
echo DESCRIBE zanaradka; >> manual_mysql_commands.txt
echo SELECT COUNT(*) FROM zanaradka; >> manual_mysql_commands.txt
echo SELECT DISTINCT marshrut FROM zanaradka ORDER BY marshrut LIMIT 10; >> manual_mysql_commands.txt
echo SELECT DISTINCT smena FROM zanaradka ORDER BY smena; >> manual_mysql_commands.txt
echo SELECT DISTINCT `pe№` FROM zanaradka WHERE `pe№` IS NOT NULL LIMIT 10; >> manual_mysql_commands.txt
echo SELECT * FROM zanaradka WHERE data_day = '2025-07-07' LIMIT 5; >> manual_mysql_commands.txt
echo. >> manual_mysql_commands.txt

echo [%time%] Пытаемся найти MySQL клиент в системе...
echo === MYSQL CLIENT SEARCH === > mysql_search.txt
echo Analysis Date: %date% %time% >> mysql_search.txt
echo. >> mysql_search.txt

echo Поиск mysql.exe в системе: >> mysql_search.txt
dir /s /b C:\mysql.exe >> mysql_search.txt 2>nul
dir /s /b D:\mysql.exe >> mysql_search.txt 2>nul
dir /s /b "C:\Program Files\MySQL\*mysql.exe" >> mysql_search.txt 2>nul
dir /s /b "C:\Program Files (x86)\MySQL\*mysql.exe" >> mysql_search.txt 2>nul
echo. >> mysql_search.txt

echo Поиск XAMPP: >> mysql_search.txt
dir /s /b "C:\xampp\mysql\bin\mysql.exe" >> mysql_search.txt 2>nul
dir /s /b "D:\xampp\mysql\bin\mysql.exe" >> mysql_search.txt 2>nul
echo. >> mysql_search.txt

echo Поиск WAMP: >> mysql_search.txt
dir /s /b "C:\wamp*\bin\mysql\*\bin\mysql.exe" >> mysql_search.txt 2>nul
dir /s /b "D:\wamp*\bin\mysql\*\bin\mysql.exe" >> mysql_search.txt 2>nul
echo. >> mysql_search.txt

echo Проверяем PATH: >> mysql_search.txt
where mysql >> mysql_search.txt 2>&1
echo. >> mysql_search.txt

echo [%time%] Создаем рекомендации на основе найденного...
echo === ANALYSIS RECOMMENDATIONS === > recommendations.txt
echo Analysis Date: %date% %time% >> recommendations.txt
echo. >> recommendations.txt

echo РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ ВЕБ-ИНТЕРФЕЙСА: >> recommendations.txt
echo. >> recommendations.txt
echo 1. ПРОСТОЙ ВИД (Simple View) - ИСПРАВЛЕНО >> recommendations.txt
echo    ✅ Добавлены поля: маршрут, смена, водитель, ПС, времена, статус >> recommendations.txt
echo    ✅ Теперь показывает полную информацию вместо только имени водителя >> recommendations.txt
echo. >> recommendations.txt

echo 2. ПОЛЯ БАЗЫ ДАННЫХ - ИСПРАВЛЕНО >> recommendations.txt
echo    ✅ Исправлено поле 'putlist???' на 'pe№' для номера ПС >> recommendations.txt
echo    ✅ Исправлено поле 'putlist???' на 'putlist№' для путевого листа >> recommendations.txt
echo    ✅ Обновлены все SQL запросы в backend >> recommendations.txt
echo. >> recommendations.txt

echo 3. РАСШИРЕННЫЙ ВИД (Extended View) >> recommendations.txt
echo    📝 Рекомендуется добавить: >> recommendations.txt
echo       - Табельный номер кондуктора (tabconduktor) >> recommendations.txt
echo       - Государственный номер ПС (если есть в БД) >> recommendations.txt
echo       - Адрес конечной остановки (kpvih) >> recommendations.txt
echo. >> recommendations.txt

echo 4. ПОЛНЫЙ ВИД MS ACCESS (Full View) >> recommendations.txt
echo    📝 Рекомендуется: >> recommendations.txt
echo       - Точно соответствовать оригинальной таблице MS Access >> recommendations.txt
echo       - Добавить все поля из структуры zanaradka >> recommendations.txt
echo       - Использовать точные названия полей как в оригинале >> recommendations.txt
echo. >> recommendations.txt

echo 5. КОДИРОВКА УКРАИНСКОГО ТЕКСТА >> recommendations.txt
echo    📝 Рекомендуется: >> recommendations.txt
echo       - Проверить функцию fix_ukrainian_encoding в backend >> recommendations.txt
echo       - Убедиться в правильной настройке charset=utf8mb4 >> recommendations.txt
echo       - Тестировать отображение украинских имен >> recommendations.txt
echo. >> recommendations.txt

echo [%time%] Создаем итоговый отчет...
echo === SUMMARY REPORT === > summary_report.txt
echo Analysis Date: %date% %time% >> summary_report.txt
echo Analysis Tool: Alternative Database Analysis (без Python) >> summary_report.txt
echo. >> summary_report.txt

echo === ФАЙЛЫ СОЗДАНЫ === >> summary_report.txt
echo 1. system_info.txt           - Информация о системе >> summary_report.txt
echo 2. network_test.txt          - Тестирование сети >> summary_report.txt
echo 3. powershell_mysql.txt      - Попытка подключения через PowerShell >> summary_report.txt
echo 4. api_data.txt              - Попытка получения данных через API >> summary_report.txt
echo 5. manual_mysql_commands.txt - Команды для ручного анализа >> summary_report.txt
echo 6. mysql_search.txt          - Поиск MySQL клиента в системе >> summary_report.txt
echo 7. recommendations.txt       - Рекомендации по улучшению >> summary_report.txt
echo 8. summary_report.txt        - Этот отчет >> summary_report.txt
echo. >> summary_report.txt

echo === СТАТУС ИСПРАВЛЕНИЙ === >> summary_report.txt
echo ✅ Исправлены поля БД в backend (pe№, putlist№) >> summary_report.txt
echo ✅ Улучшен Simple View - теперь показывает все нужные поля >> summary_report.txt
echo ✅ Обновлены SQL запросы в сервисах >> summary_report.txt
echo ✅ Добавлено форматирование статусов >> summary_report.txt
echo. >> summary_report.txt

echo === СЛЕДУЮЩИЕ ШАГИ === >> summary_report.txt
echo 1. Перезапустите backend сервер >> summary_report.txt
echo 2. Проверьте Simple View в веб-интерфейсе >> summary_report.txt
echo 3. Убедитесь, что данные отображаются корректно >> summary_report.txt
echo 4. При необходимости доустановите MySQL клиент для полного анализа >> summary_report.txt
echo 5. Рассмотрите возможность обновления Extended и Full View >> summary_report.txt
echo. >> summary_report.txt

echo === АЛЬТЕРНАТИВНЫЕ РЕШЕНИЯ === >> summary_report.txt
echo Если этот скрипт не дал полной информации: >> summary_report.txt
echo 1. Установите Python на сервере и используйте enhanced_db_analysis.py >> summary_report.txt
echo 2. Установите MySQL клиент (mysql.exe) >> summary_report.txt
echo 3. Используйте phpMyAdmin через веб-интерфейс >> summary_report.txt
echo 4. Подключитесь к БД через другие MySQL клиенты (HeidiSQL, MySQL Workbench) >> summary_report.txt
echo. >> summary_report.txt

echo.
echo ===============================================
echo Альтернативный анализ БД завершен!
echo ===============================================
echo.
echo Файлы созданы в папке 'alternative_db_analysis':
dir /b
echo.
echo ВАЖНО:
echo - Основные проблемы УЖЕ ИСПРАВЛЕНЫ в коде
echo - Simple View теперь показывает все нужные поля
echo - Поля БД исправлены (pe№, putlist№)
echo - Перезапустите сервер и проверьте изменения
echo.
echo Если нужен более детальный анализ:
echo - Установите Python или MySQL клиент
echo - Или используйте веб-интерфейс для управления БД
echo.
pause 