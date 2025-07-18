@echo off
echo ===============================================
echo DISPATCHER DATABASE ANALYSIS TOOL
echo Analyzing MS Access database structure
echo ===============================================
echo.

echo [%time%] Starting dispatcher database analysis...

REM Create output folder
if not exist "dispatcher_analysis_results" mkdir "dispatcher_analysis_results"
cd "dispatcher_analysis_results"

echo [%time%] Collecting database connection info...
echo === DATABASE CONNECTION INFO === > connection_info.txt
echo Analysis Date: %date% %time% >> connection_info.txt
echo Remote MySQL Server: 91.222.248.216:61315 >> connection_info.txt
echo Database: saltdepoavt_ >> connection_info.txt
echo User: khtrm_remote >> connection_info.txt
echo. >> connection_info.txt

echo [%time%] Testing database connection...
echo Testing connection to remote MySQL server... >> connection_info.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" -e "SELECT VERSION();" >> connection_info.txt 2>&1
echo. >> connection_info.txt

echo [%time%] Analyzing ZANARADKA table structure...
echo === ZANARADKA TABLE ANALYSIS === > zanaradka_analysis.txt
echo Analysis Date: %date% %time% >> zanaradka_analysis.txt
echo. >> zanaradka_analysis.txt

echo Table structure: >> zanaradka_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE zanaradka;" >> zanaradka_analysis.txt 2>&1
echo. >> zanaradka_analysis.txt

echo Table indexes: >> zanaradka_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SHOW INDEX FROM zanaradka;" >> zanaradka_analysis.txt 2>&1
echo. >> zanaradka_analysis.txt

echo Row count: >> zanaradka_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT COUNT(*) as total_rows FROM zanaradka;" >> zanaradka_analysis.txt 2>&1
echo. >> zanaradka_analysis.txt

echo Sample data (first 10 rows): >> zanaradka_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM zanaradka LIMIT 10;" >> zanaradka_analysis.txt 2>&1
echo. >> zanaradka_analysis.txt

echo Recent data (last 10 rows): >> zanaradka_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM zanaradka ORDER BY key DESC LIMIT 10;" >> zanaradka_analysis.txt 2>&1
echo. >> zanaradka_analysis.txt

echo Data for date 2025-07-07 (if exists): >> zanaradka_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM zanaradka WHERE data_day = '2025-07-07' LIMIT 10;" >> zanaradka_analysis.txt 2>&1
echo. >> zanaradka_analysis.txt

echo [%time%] Analyzing related tables...
echo === RELATED TABLES ANALYSIS === > related_tables.txt
echo Analysis Date: %date% %time% >> related_tables.txt
echo. >> related_tables.txt

echo SPRMARSHRUT table (routes): >> related_tables.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE sprmarshrut;" >> related_tables.txt 2>&1
echo. >> related_tables.txt
echo Sample routes data: >> related_tables.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM sprmarshrut LIMIT 10;" >> related_tables.txt 2>&1
echo. >> related_tables.txt

echo SPRPERSONAL table (personnel): >> related_tables.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE sprpersonal;" >> related_tables.txt 2>&1
echo. >> related_tables.txt
echo Sample personnel data: >> related_tables.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM sprpersonal LIMIT 10;" >> related_tables.txt 2>&1
echo. >> related_tables.txt

echo SPRPE table (vehicles): >> related_tables.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "DESCRIBE sprpe;" >> related_tables.txt 2>&1
echo. >> related_tables.txt
echo Sample vehicle data: >> related_tables.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT * FROM sprpe LIMIT 10;" >> related_tables.txt 2>&1
echo. >> related_tables.txt

echo [%time%] Analyzing field meanings and relationships...
echo === FIELD ANALYSIS === > field_analysis.txt
echo Analysis Date: %date% %time% >> field_analysis.txt
echo. >> field_analysis.txt

echo Unique values in key fields: >> field_analysis.txt
echo. >> field_analysis.txt

echo MARSHRUT field (route numbers): >> field_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT DISTINCT marshrut FROM zanaradka ORDER BY marshrut LIMIT 20;" >> field_analysis.txt 2>&1
echo. >> field_analysis.txt

echo VIPUSK field (release numbers): >> field_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT DISTINCT vipusk FROM zanaradka ORDER BY vipusk LIMIT 20;" >> field_analysis.txt 2>&1
echo. >> field_analysis.txt

echo SMENA field (shifts): >> field_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT DISTINCT smena FROM zanaradka ORDER BY smena;" >> field_analysis.txt 2>&1
echo. >> field_analysis.txt

echo TABVODITEL field (driver tab numbers): >> field_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT DISTINCT tabvoditel FROM zanaradka WHERE tabvoditel IS NOT NULL ORDER BY tabvoditel LIMIT 20;" >> field_analysis.txt 2>&1
echo. >> field_analysis.txt

echo PE№ field (vehicle numbers): >> field_analysis.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT DISTINCT pe№ FROM zanaradka WHERE pe№ IS NOT NULL ORDER BY pe№ LIMIT 20;" >> field_analysis.txt 2>&1
echo. >> field_analysis.txt

echo [%time%] Analyzing data patterns...
echo === DATA PATTERNS === > data_patterns.txt
echo Analysis Date: %date% %time% >> data_patterns.txt
echo. >> data_patterns.txt

echo Recent assignments pattern: >> data_patterns.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT marshrut, vipusk, smena, fiovoditel, pe№, data_day FROM zanaradka WHERE data_day >= '2025-07-01' ORDER BY data_day DESC LIMIT 15;" >> data_patterns.txt 2>&1
echo. >> data_patterns.txt

echo Daily assignment count: >> data_patterns.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT data_day, COUNT(*) as assignments_count FROM zanaradka WHERE data_day >= '2025-07-01' GROUP BY data_day ORDER BY data_day DESC LIMIT 10;" >> data_patterns.txt 2>&1
echo. >> data_patterns.txt

echo Routes with most assignments: >> data_patterns.txt
mysql -h 91.222.248.216 -P 61315 -u khtrm_remote -p"KhTRM_2025!" saltdepoavt_ -e "SELECT marshrut, COUNT(*) as count FROM zanaradka WHERE data_day >= '2025-07-01' GROUP BY marshrut ORDER BY count DESC LIMIT 10;" >> data_patterns.txt 2>&1
echo. >> data_patterns.txt

echo [%time%] Creating field mapping...
echo === FIELD MAPPING === > field_mapping.txt
echo Analysis Date: %date% %time% >> field_mapping.txt
echo. >> field_mapping.txt
echo Field mapping from MS Access to web interface: >> field_mapping.txt
echo. >> field_mapping.txt
echo MS Access Field -> Web Interface Field -> Description >> field_mapping.txt
echo ================================================== >> field_mapping.txt
echo marshrut -> Route Number -> Номер маршрута >> field_mapping.txt
echo vipusk -> Release -> Выпуск >> field_mapping.txt
echo smena -> Shift -> Смена >> field_mapping.txt
echo tabvoditel -> Driver Tab -> Табельный номер водителя >> field_mapping.txt
echo fiovoditel -> Driver Name -> ФИО водителя >> field_mapping.txt
echo tabconduktor -> Conductor Tab -> Табельный номер кондуктора >> field_mapping.txt
echo fioconduktor -> Conductor Name -> ФИО кондуктора >> field_mapping.txt
echo pe№ -> Vehicle Number -> Номер подвижного состава >> field_mapping.txt
echo data_day -> Date -> Дата наряда >> field_mapping.txt
echo tvih -> Departure Time -> Время выхода >> field_mapping.txt
echo tzah -> Arrival Time -> Время захода >> field_mapping.txt
echo putlist№ -> Waybill Number -> Номер путевого листа >> field_mapping.txt
echo. >> field_mapping.txt

echo [%time%] Creating summary report...
echo === DISPATCHER ANALYSIS SUMMARY === > summary_report.txt
echo Analysis Date: %date% %time% >> summary_report.txt
echo Analysis Tool: Dispatcher Database Analysis >> summary_report.txt
echo. >> summary_report.txt
echo Files Created: >> summary_report.txt
echo - connection_info.txt     : Database connection details >> summary_report.txt
echo - zanaradka_analysis.txt  : Main assignments table analysis >> summary_report.txt
echo - related_tables.txt      : Related tables structure >> summary_report.txt
echo - field_analysis.txt      : Field values and patterns >> summary_report.txt
echo - data_patterns.txt       : Data patterns and statistics >> summary_report.txt
echo - field_mapping.txt       : Field mapping documentation >> summary_report.txt
echo - summary_report.txt      : This summary >> summary_report.txt
echo. >> summary_report.txt
echo Key Findings: >> summary_report.txt
echo - Total tables analyzed: 4 (zanaradka, sprmarshrut, sprpersonal, sprpe) >> summary_report.txt
echo - Main assignments table: zanaradka >> summary_report.txt
echo - Key fields for web interface identified >> summary_report.txt
echo. >> summary_report.txt
echo Next Steps: >> summary_report.txt
echo 1. Review all generated analysis files >> summary_report.txt
echo 2. Update web interface based on field mapping >> summary_report.txt
echo 3. Implement extended table with all relevant columns >> summary_report.txt
echo 4. Test data integration with real database >> summary_report.txt
echo. >> summary_report.txt

echo.
echo ===============================================
echo Dispatcher database analysis completed!
echo ===============================================
echo.
echo Files created in 'dispatcher_analysis_results' folder:
dir /b
echo.
echo IMPORTANT: 
echo - Review all analysis files carefully
echo - Use field_mapping.txt for web interface development
echo - Archive and send results to development team
echo.
pause 