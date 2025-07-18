@echo off
chcp 65001 >nul
echo ===============================================
echo PYTHON DATABASE ANALYSIS TOOL
echo Инструмент для анализа базы данных диспетчера
echo ===============================================
echo.

echo [%time%] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден. Пожалуйста, установите Python 3.8 или выше.
    pause
    exit /b 1
)

echo [%time%] Проверка pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip не найден. Пожалуйста, установите pip.
    pause
    exit /b 1
)

echo [%time%] Установка зависимостей...
echo Устанавливаем mysql-connector-python...
pip install mysql-connector-python
if %errorlevel% neq 0 (
    echo ❌ Не удалось установить mysql-connector-python
    echo Попробуйте установить вручную: pip install mysql-connector-python
    pause
    exit /b 1
)

echo [%time%] Запуск анализа базы данных...
echo.
echo 🚀 Запускаем Python-скрипт для анализа...
echo.

python enhanced_db_analysis.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при запуске анализа
    echo Проверьте:
    echo 1. Подключение к интернету
    echo 2. Доступность базы данных
    echo 3. Правильность настроек подключения
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ Анализ завершен!
echo ===============================================
echo.
echo Проверьте папку 'python_db_analysis' для результатов:
echo - full_analysis.json (для программной обработки)
echo - analysis_report.txt (читаемый отчет)
echo.
echo Следующие шаги:
echo 1. Изучите analysis_report.txt
echo 2. Сообщите о находках разработчику
echo 3. Используйте рекомендации для улучшения веб-интерфейса
echo.
pause 