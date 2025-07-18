@echo off
echo ===============================================
echo MS Access Data Collection Tool
echo Simple batch version (no Python required)
echo ===============================================
echo.

echo [%time%] Starting data collection...

REM Create output folder
if not exist "data_collection_results" mkdir "data_collection_results"
cd "data_collection_results"

echo [%time%] Collecting system information...
echo === SYSTEM INFORMATION === > system_info.txt
echo Collection Date: %date% %time% >> system_info.txt
echo. >> system_info.txt
echo Hostname: >> system_info.txt
hostname >> system_info.txt
echo. >> system_info.txt
echo OS Version: >> system_info.txt
ver >> system_info.txt
echo. >> system_info.txt
echo Current User: >> system_info.txt
whoami >> system_info.txt
echo. >> system_info.txt
echo Current Directory: >> system_info.txt
cd >> system_info.txt
echo. >> system_info.txt
echo Network Configuration: >> system_info.txt
ipconfig /all >> system_info.txt
echo. >> system_info.txt
echo Disk Information: >> system_info.txt
wmic logicaldisk get size,freespace,caption >> system_info.txt
echo. >> system_info.txt
echo Running Processes: >> system_info.txt
tasklist >> system_info.txt

echo [%time%] Searching for MS Access files...
echo === MS ACCESS FILES === > access_files.txt
echo Collection Date: %date% %time% >> access_files.txt
echo. >> access_files.txt
echo Searching C: drive for .mdb files... >> access_files.txt
dir /s /b C:\*.mdb >> access_files.txt 2>nul
echo. >> access_files.txt
echo Searching C: drive for .accdb files... >> access_files.txt
dir /s /b C:\*.accdb >> access_files.txt 2>nul
echo. >> access_files.txt
echo Searching D: drive for .mdb files... >> access_files.txt
dir /s /b D:\*.mdb >> access_files.txt 2>nul
echo. >> access_files.txt
echo Searching D: drive for .accdb files... >> access_files.txt
dir /s /b D:\*.accdb >> access_files.txt 2>nul
echo. >> access_files.txt
echo Searching for .mde files... >> access_files.txt
dir /s /b C:\*.mde >> access_files.txt 2>nul
dir /s /b D:\*.mde >> access_files.txt 2>nul
echo. >> access_files.txt
echo Searching for .accde files... >> access_files.txt
dir /s /b C:\*.accde >> access_files.txt 2>nul
dir /s /b D:\*.accde >> access_files.txt 2>nul

echo [%time%] Testing MySQL connection...
echo === MYSQL CONNECTION TEST === > mysql_test.txt
echo Collection Date: %date% %time% >> mysql_test.txt
echo. >> mysql_test.txt
echo Testing MySQL connection method 1... >> mysql_test.txt
mysql -u khtrm_remote -p"KhTRM_2025!" -e "SHOW DATABASES;" >> mysql_test.txt 2>&1
echo. >> mysql_test.txt
echo Testing MySQL connection method 2... >> mysql_test.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" -e "SHOW DATABASES;" >> mysql_test.txt 2>&1
echo. >> mysql_test.txt
echo Testing MySQL connection method 3... >> mysql_test.txt
mysql -h 127.0.0.1 -u khtrm_remote -p"KhTRM_2025!" -e "SHOW DATABASES;" >> mysql_test.txt 2>&1

echo [%time%] Getting table information...
echo === MYSQL TABLES === > mysql_tables.txt
echo Collection Date: %date% %time% >> mysql_tables.txt
echo. >> mysql_tables.txt
echo Tables in saltdepoavt_ database: >> mysql_tables.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SHOW TABLES;" >> mysql_tables.txt 2>&1
echo. >> mysql_tables.txt
echo Structure of key tables: >> mysql_tables.txt
echo. >> mysql_tables.txt
echo === ZANARADKA TABLE STRUCTURE === >> mysql_tables.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE zanaradka;" >> mysql_tables.txt 2>&1
echo. >> mysql_tables.txt
echo === SPRMARSHRUT TABLE STRUCTURE === >> mysql_tables.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE sprmarshrut;" >> mysql_tables.txt 2>&1
echo. >> mysql_tables.txt
echo === SPRPERSONAL TABLE STRUCTURE === >> mysql_tables.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE sprpersonal;" >> mysql_tables.txt 2>&1
echo. >> mysql_tables.txt
echo === SPRPE TABLE STRUCTURE === >> mysql_tables.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE sprpe;" >> mysql_tables.txt 2>&1

echo [%time%] Getting sample data...
echo === SAMPLE DATA === > sample_data.txt
echo Collection Date: %date% %time% >> sample_data.txt
echo. >> sample_data.txt
echo Sample data from zanaradka (first 5 rows): >> sample_data.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM zanaradka LIMIT 5;" >> sample_data.txt 2>&1
echo. >> sample_data.txt
echo Sample data from sprmarshrut (first 5 rows): >> sample_data.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM sprmarshrut LIMIT 5;" >> sample_data.txt 2>&1
echo. >> sample_data.txt
echo Sample data from sprpersonal (first 5 rows): >> sample_data.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM sprpersonal LIMIT 5;" >> sample_data.txt 2>&1
echo. >> sample_data.txt
echo Sample data from sprpe (first 5 rows): >> sample_data.txt
mysql -h localhost -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM sprpe LIMIT 5;" >> sample_data.txt 2>&1

echo [%time%] Searching for database files...
echo === DATABASE FILES === > database_files.txt
echo Collection Date: %date% %time% >> database_files.txt
echo. >> database_files.txt
echo Searching for SQL files... >> database_files.txt
dir /s /b C:\*.sql >> database_files.txt 2>nul
dir /s /b D:\*.sql >> database_files.txt 2>nul
echo. >> database_files.txt
echo Searching for backup files... >> database_files.txt
dir /s /b C:\*.bak >> database_files.txt 2>nul
dir /s /b D:\*.bak >> database_files.txt 2>nul
dir /s /b C:\*.backup >> database_files.txt 2>nul
dir /s /b D:\*.backup >> database_files.txt 2>nul
echo. >> database_files.txt
echo Searching for configuration files... >> database_files.txt
dir /s /b C:\*.ini >> database_files.txt 2>nul
dir /s /b D:\*.ini >> database_files.txt 2>nul
dir /s /b C:\*.cfg >> database_files.txt 2>nul
dir /s /b D:\*.cfg >> database_files.txt 2>nul
dir /s /b C:\*.conf >> database_files.txt 2>nul
dir /s /b D:\*.conf >> database_files.txt 2>nul

echo [%time%] Creating summary report...
echo === DATA COLLECTION SUMMARY === > summary_report.txt
echo Collection Date: %date% %time% >> summary_report.txt
echo Collection Tool: Simple Batch Version >> summary_report.txt
echo. >> summary_report.txt
echo Files Created: >> summary_report.txt
echo - system_info.txt       : System information >> summary_report.txt
echo - access_files.txt      : MS Access files found >> summary_report.txt
echo - mysql_test.txt        : MySQL connection tests >> summary_report.txt
echo - mysql_tables.txt      : Database table structures >> summary_report.txt
echo - sample_data.txt       : Sample data from key tables >> summary_report.txt
echo - database_files.txt    : Other database files found >> summary_report.txt
echo - summary_report.txt    : This summary >> summary_report.txt
echo. >> summary_report.txt
echo Next Steps: >> summary_report.txt
echo 1. Review all generated .txt files >> summary_report.txt
echo 2. Archive the 'data_collection_results' folder >> summary_report.txt
echo 3. Send the archive to the development team >> summary_report.txt
echo 4. Delete sensitive files after use >> summary_report.txt
echo. >> summary_report.txt

echo.
echo ===============================================
echo Data collection completed successfully!
echo ===============================================
echo.
echo Files created in 'data_collection_results' folder:
dir /b
echo.
echo IMPORTANT: 
echo - Review the files for sensitive information
echo - Archive the folder and send to development team
echo - Delete this folder after use for security
echo.
pause 