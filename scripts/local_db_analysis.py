#!/usr/bin/env python3
"""
Local Database Analysis Tool
Локальный анализ удаленной базы данных диспетчера
"""

import json
import os
import sys
from datetime import datetime
from typing import Any

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("❌ Ошибка: Не найден модуль mysql-connector-python")
    print("Установите его командой: pip install mysql-connector-python")
    sys.exit(1)


class LocalDatabaseAnalyzer:
    """Класс для локального анализа удаленной базы данных диспетчера"""

    def __init__(self):
        """Инициализация с настройками подключения к удаленной БД"""
        self.config = {
            "host": "91.222.248.216",
            "port": 61315,
            "user": "khtrm_remote",
            "password": "KhTRM_2025!",
            "database": "saltdepoavt_",
            "charset": "utf8mb4",
            "use_unicode": True,
            "autocommit": True,
            "connect_timeout": 30,
            "buffered": True,
        }
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        """Подключение к удаленной базе данных"""
        try:
            print(f"🔗 Подключение к {self.config['host']}:{self.config['port']}...")
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True, buffered=True)
            print("✅ Успешное подключение к удаленной базе данных")

            # Проверяем версию сервера
            self.cursor.execute("SELECT VERSION() as version")
            version_info = self.cursor.fetchone()
            print(f"📊 Версия MySQL сервера: {version_info['version']}")

            return True
        except Error as e:
            print(f"❌ Ошибка подключения к базе данных: {e}")
            return False

    def disconnect(self):
        """Отключение от базы данных"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("📝 Соединение с базой данных закрыто")

    def get_all_tables(self) -> list[str]:
        """Получение списка всех таблиц в БД"""
        try:
            self.cursor.execute("SHOW TABLES")
            tables = [
                row[f"Tables_in_{self.config['database']}"]
                for row in self.cursor.fetchall()
            ]
            return tables
        except Error as e:
            print(f"❌ Ошибка получения списка таблиц: {e}")
            return []

    def get_table_structure_detailed(self, table_name: str) -> dict[str, Any]:
        """Получение детальной структуры таблицы"""
        try:
            # Основная структура
            self.cursor.execute(f"DESCRIBE {table_name}")
            basic_structure = self.cursor.fetchall()

            # Подробная информация о столбцах
            self.cursor.execute(f"""
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    COLUMN_TYPE,
                    COLUMN_COMMENT,
                    ORDINAL_POSITION,
                    CHARACTER_MAXIMUM_LENGTH,
                    NUMERIC_PRECISION,
                    NUMERIC_SCALE
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = '{self.config["database"]}'
                AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            detailed_structure = self.cursor.fetchall()

            # Индексы
            self.cursor.execute(f"SHOW INDEX FROM {table_name}")
            indexes = self.cursor.fetchall()

            # Количество записей
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count_result = self.cursor.fetchone()
            row_count = count_result["count"] if count_result else 0

            # Статистика по данным
            self.cursor.execute(f"""
                SELECT
                    MIN(STR_TO_DATE(data_day, '%Y-%m-%d')) as min_date,
                    MAX(STR_TO_DATE(data_day, '%Y-%m-%d')) as max_date,
                    COUNT(DISTINCT data_day) as unique_dates
                FROM {table_name}
                WHERE data_day IS NOT NULL
            """)
            date_stats = self.cursor.fetchone()

            return {
                "basic_structure": basic_structure,
                "detailed_structure": detailed_structure,
                "indexes": indexes,
                "row_count": row_count,
                "date_statistics": date_stats,
            }

        except Error as e:
            print(f"❌ Ошибка получения структуры таблицы {table_name}: {e}")
            return {}

    def analyze_field_relationships(self, table_name: str) -> dict[str, Any]:
        """Анализ связей между полями"""
        try:
            # Ключевые поля для анализа связей
            analysis_fields = [
                "marshrut",
                "vipusk",
                "smena",
                "tabvoditel",
                "fiovoditel",
                "tabconduktor",
                "fioconduktor",
                "pe№",
                "putlist№",
                "data_day",
            ]

            relationships = {}

            for field in analysis_fields:
                print(f"   📊 Анализирую поле: {field}")

                # Уникальные значения и их частота
                try:
                    field_query = f"`{field}`" if "№" in field else field

                    self.cursor.execute(f"""
                        SELECT {field_query} as value, COUNT(*) as count
                        FROM {table_name}
                        WHERE {field_query} IS NOT NULL
                        AND {field_query} != ''
                        GROUP BY {field_query}
                        ORDER BY count DESC, {field_query} ASC
                        LIMIT 50
                    """)
                    unique_values = self.cursor.fetchall()

                    # Статистика по полю
                    self.cursor.execute(f"""
                        SELECT
                            COUNT(DISTINCT {field_query}) as unique_count,
                            COUNT({field_query}) as non_null_count,
                            COUNT(*) as total_count
                        FROM {table_name}
                    """)
                    field_stats = self.cursor.fetchone()

                    relationships[field] = {
                        "unique_values": unique_values,
                        "statistics": field_stats,
                    }

                except Error as e:
                    print(f"   ⚠️ Ошибка анализа поля {field}: {e}")
                    relationships[field] = {"error": str(e)}

            return relationships

        except Error as e:
            print(f"❌ Ошибка анализа связей полей: {e}")
            return {}

    def analyze_data_patterns(self, table_name: str) -> dict[str, Any]:
        """Анализ паттернов данных"""
        try:
            patterns = {}

            # Анализ по датам
            print("   📅 Анализ данных по датам...")
            self.cursor.execute(f"""
                SELECT
                    data_day,
                    COUNT(*) as assignments_count,
                    COUNT(DISTINCT marshrut) as routes_count,
                    COUNT(DISTINCT smena) as shifts_count,
                    COUNT(DISTINCT tabvoditel) as drivers_count
                FROM {table_name}
                WHERE data_day >= '2025-07-01'
                GROUP BY data_day
                ORDER BY data_day DESC
                LIMIT 15
            """)
            date_patterns = self.cursor.fetchall()
            patterns["by_date"] = date_patterns

            # Анализ по маршрутам
            print("   🚌 Анализ данных по маршрутам...")
            self.cursor.execute(f"""
                SELECT
                    marshrut,
                    COUNT(*) as total_assignments,
                    COUNT(DISTINCT data_day) as days_active,
                    COUNT(DISTINCT smena) as shifts_used,
                    COUNT(DISTINCT tabvoditel) as drivers_count
                FROM {table_name}
                WHERE data_day >= '2025-07-01'
                GROUP BY marshrut
                ORDER BY total_assignments DESC
                LIMIT 20
            """)
            route_patterns = self.cursor.fetchall()
            patterns["by_route"] = route_patterns

            # Анализ по сменам
            print("   ⏰ Анализ данных по сменам...")
            self.cursor.execute(f"""
                SELECT
                    smena,
                    COUNT(*) as total_assignments,
                    COUNT(DISTINCT marshrut) as routes_count,
                    COUNT(DISTINCT tabvoditel) as drivers_count,
                    AVG(TIME_TO_SEC(TIMEDIFF(tzah, tvih))/3600) as avg_work_hours
                FROM {table_name}
                WHERE data_day >= '2025-07-01'
                AND tvih IS NOT NULL
                AND tzah IS NOT NULL
                GROUP BY smena
                ORDER BY smena
            """)
            shift_patterns = self.cursor.fetchall()
            patterns["by_shift"] = shift_patterns

            return patterns

        except Error as e:
            print(f"❌ Ошибка анализа паттернов данных: {e}")
            return {}

    def analyze_ms_access_structure(self) -> dict[str, Any]:
        """Специальный анализ для понимания структуры MS Access"""
        try:
            print("🔍 Анализ структуры MS Access...")

            # Получаем примеры данных для понимания структуры
            self.cursor.execute("""
                SELECT * FROM zanaradka
                WHERE data_day = '2025-07-07'
                ORDER BY marshrut, smena
                LIMIT 5
            """)
            sample_data = self.cursor.fetchall()

            # Анализируем все поля таблицы zanaradka
            self.cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, COLUMN_TYPE, COLUMN_COMMENT
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = 'saltdepoavt_'
                AND TABLE_NAME = 'zanaradka'
                ORDER BY ORDINAL_POSITION
            """)
            all_fields = self.cursor.fetchall()

            # Проверяем какие поля содержат данные
            fields_with_data = {}
            for field_info in all_fields:
                field_name = field_info["COLUMN_NAME"]
                field_query = f"`{field_name}`" if "№" in field_name else field_name

                try:
                    self.cursor.execute(f"""
                        SELECT COUNT(*) as total,
                               COUNT({field_query}) as non_null,
                               COUNT(DISTINCT {field_query}) as unique_vals
                        FROM zanaradka
                        WHERE data_day >= '2025-07-01'
                    """)
                    field_stats = self.cursor.fetchone()
                    fields_with_data[field_name] = field_stats
                except Exception:
                    fields_with_data[field_name] = {"error": "Cannot analyze field"}

            return {
                "sample_data": sample_data,
                "all_fields": all_fields,
                "fields_with_data": fields_with_data,
            }

        except Error as e:
            print(f"❌ Ошибка анализа структуры MS Access: {e}")
            return {}

    def create_field_mapping_enhanced(self) -> dict[str, Any]:
        """Создание расширенной карты полей"""
        print("🗺️ Создание расширенной карты полей...")

        # Полная карта полей на основе анализа структуры MS Access
        field_mapping = {
            # Основные идентификаторы
            "key": {
                "web_field": "id",
                "description": "Уникальный ID записи",
                "type": "primary_key",
            },
            "data_day": {
                "web_field": "assignment_date",
                "description": "Дата наряда",
                "type": "date",
            },
            # Информация о маршруте и смене
            "marshrut": {
                "web_field": "route_number",
                "description": "Номер маршрута",
                "type": "route_info",
            },
            "vipusk": {
                "web_field": "brigade",
                "description": "Бригада/Выпуск",
                "type": "route_info",
            },
            "smena": {
                "web_field": "shift",
                "description": "Смена",
                "type": "shift_info",
            },
            # Персонал
            "tabvoditel": {
                "web_field": "driver_tab_number",
                "description": "Табельный номер водителя",
                "type": "personnel",
            },
            "fiovoditel": {
                "web_field": "driver_name",
                "description": "ФИО водителя",
                "type": "personnel",
            },
            "tabconduktor": {
                "web_field": "conductor_tab_number",
                "description": "Табельный номер кондуктора",
                "type": "personnel",
            },
            "fioconduktor": {
                "web_field": "conductor_name",
                "description": "ФИО кондуктора",
                "type": "personnel",
            },
            # Подвижной состав
            "pe№": {
                "web_field": "vehicle_number",
                "description": "Номер подвижного состава",
                "type": "vehicle",
            },
            "putlist№": {
                "web_field": "waybill_number",
                "description": "Номер путевого листа",
                "type": "documents",
            },
            # Время
            "tvih": {
                "web_field": "departure_time",
                "description": "Время выхода",
                "type": "schedule",
            },
            "tzah": {
                "web_field": "arrival_time",
                "description": "Время захода",
                "type": "schedule",
            },
            # Дополнительные поля
            "ZaprAdr": {
                "web_field": "fuel_address",
                "description": "Адрес заправки",
                "type": "logistics",
            },
            "kpvih": {
                "web_field": "route_endpoint",
                "description": "Конечная остановка",
                "type": "route_info",
            },
            "tipvipusk": {
                "web_field": "route_type",
                "description": "Тип выпуска",
                "type": "route_info",
            },
        }

        # Группировка полей по категориям для разных видов отображения
        view_configurations = {
            "simple": {
                "description": "Простой вид - основные поля",
                "fields": [
                    "route_number",
                    "shift",
                    "driver_name",
                    "vehicle_number",
                    "departure_time",
                    "arrival_time",
                    "status",
                ],
            },
            "extended": {
                "description": "Расширенный вид - детальная информация",
                "fields": [
                    "route_number",
                    "brigade",
                    "shift",
                    "driver_tab_number",
                    "driver_name",
                    "conductor_name",
                    "vehicle_number",
                    "departure_time",
                    "arrival_time",
                    "waybill_number",
                    "fuel_address",
                    "route_endpoint",
                    "status",
                ],
            },
            "full_ms_access": {
                "description": "Полный вид MS Access - все поля",
                "fields": list(field_mapping.keys()),
            },
        }

        return {
            "field_mapping": field_mapping,
            "view_configurations": view_configurations,
            "total_fields": len(field_mapping),
        }

    def save_analysis_results(
        self, analysis_data: dict[str, Any], output_dir: str = "local_db_analysis"
    ):
        """Сохранение результатов анализа"""
        print(f"💾 Сохранение результатов в папку: {output_dir}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON для программной обработки
        with open(
            os.path.join(output_dir, f"full_analysis_{timestamp}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2, default=str)

        # Читаемый отчет
        with open(
            os.path.join(output_dir, f"analysis_report_{timestamp}.txt"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("=== ЛОКАЛЬНЫЙ АНАЛИЗ УДАЛЕННОЙ БАЗЫ ДАННЫХ ===\n")
            f.write(f"Дата анализа: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write(f"Сервер: {self.config['host']}:{self.config['port']}\n")
            f.write(f"База данных: {self.config['database']}\n\n")

            # Общая информация
            f.write("=== ОБЩАЯ ИНФОРМАЦИЯ ===\n")
            f.write(f"Всего таблиц в БД: {len(analysis_data.get('all_tables', []))}\n")
            zanaradka_data = analysis_data.get("zanaradka_analysis", {})
            structure = zanaradka_data.get("structure", {})
            f.write(f"Записей в zanaradka: {structure.get('row_count', 0)}\n\n")

            # Структура таблицы
            f.write("=== СТРУКТУРА ТАБЛИЦЫ ZANARADKA ===\n")
            if structure.get("detailed_structure"):
                for field in structure["detailed_structure"]:
                    f.write(f"{field['COLUMN_NAME']}: {field['COLUMN_TYPE']}")
                    if field["COLUMN_COMMENT"]:
                        f.write(f" -- {field['COLUMN_COMMENT']}")
                    f.write("\n")
                f.write("\n")

            # MS Access структура
            ms_access = analysis_data.get("ms_access_analysis", {})
            if ms_access.get("all_fields"):
                f.write("=== АНАЛИЗ ПОЛЕЙ MS ACCESS ===\n")
                for field in ms_access["all_fields"]:
                    field_name = field["COLUMN_NAME"]
                    data_info = ms_access.get("fields_with_data", {}).get(
                        field_name, {}
                    )
                    if not data_info.get("error"):
                        f.write(
                            f"{field_name}: {data_info.get('non_null', 0)} записей из {data_info.get('total', 0)}\n"
                        )
                f.write("\n")

            # Карта полей
            f.write("=== КАРТА ПОЛЕЙ ===\n")
            field_mapping = analysis_data.get("enhanced_field_mapping", {}).get(
                "field_mapping", {}
            )
            for db_field, mapping_info in field_mapping.items():
                f.write(
                    f"{db_field} -> {mapping_info['web_field']} ({mapping_info['description']})\n"
                )
            f.write("\n")

            # Рекомендации
            f.write("=== РЕКОМЕНДАЦИИ ===\n")
            recommendations = analysis_data.get("recommendations", [])
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")

        print(f"✅ Результаты сохранены в {output_dir}/")

    def run_full_analysis(self):
        """Запуск полного локального анализа удаленной БД"""
        print("🚀 Запуск полного локального анализа удаленной базы данных...")
        print("=" * 70)

        if not self.connect():
            return False

        try:
            # Получаем список всех таблиц
            print("📋 Получение списка таблиц...")
            all_tables = self.get_all_tables()
            print(f"   Найдено таблиц: {len(all_tables)}")

            # Анализ основной таблицы zanaradka
            print("📊 Детальный анализ таблицы zanaradka...")
            zanaradka_structure = self.get_table_structure_detailed("zanaradka")

            # Анализ связей полей
            print("🔗 Анализ связей между полями...")
            field_relationships = self.analyze_field_relationships("zanaradka")

            # Анализ паттернов данных
            print("📈 Анализ паттернов данных...")
            data_patterns = self.analyze_data_patterns("zanaradka")

            # Специальный анализ MS Access структуры
            print("🔍 Анализ структуры MS Access...")
            ms_access_analysis = self.analyze_ms_access_structure()

            # Создание расширенной карты полей
            enhanced_field_mapping = self.create_field_mapping_enhanced()

            # Генерация рекомендаций
            recommendations = [
                "✅ Поля БД уже исправлены (pe№, putlist№)",
                "✅ Simple View уже улучшен",
                "📝 Рассмотрите добавление всех найденных полей в Full View",
                "🔧 Проверьте кодировку украинских символов",
                "📊 Добавьте статистику по данным в интерфейс",
                "🗂️ Рассмотрите группировку полей по категориям",
            ]

            # Сборка результатов
            full_analysis = {
                "timestamp": datetime.now().isoformat(),
                "database_info": {
                    "host": self.config["host"],
                    "database": self.config["database"],
                    "connection_status": "success",
                },
                "all_tables": all_tables,
                "zanaradka_analysis": {
                    "structure": zanaradka_structure,
                    "field_relationships": field_relationships,
                    "data_patterns": data_patterns,
                },
                "ms_access_analysis": ms_access_analysis,
                "enhanced_field_mapping": enhanced_field_mapping,
                "recommendations": recommendations,
            }

            # Сохранение результатов
            self.save_analysis_results(full_analysis)

            print("=" * 70)
            print("✅ Локальный анализ завершен успешно!")
            print("📁 Результаты сохранены в папке 'local_db_analysis'")
            print("📊 Основные находки:")
            print(f"   - Проанализировано {len(all_tables)} таблиц")
            print(
                f"   - Найдено {len(enhanced_field_mapping['field_mapping'])} ключевых полей"
            )
            print(
                f"   - Записей в zanaradka: {zanaradka_structure.get('row_count', 0)}"
            )
            print("   - Создана расширенная карта полей")
            print("   - Сгенерированы рекомендации по улучшению")

            return True

        except Exception as e:
            print(f"❌ Ошибка во время анализа: {e}")
            return False

        finally:
            self.disconnect()


def main():
    """Главная функция"""
    print("🔍 Local Database Analysis Tool")
    print("Локальный анализ удаленной базы данных диспетчера")
    print("=" * 70)

    # Проверка зависимостей
    print("🔧 Проверка зависимостей...")

    # Запуск анализа
    analyzer = LocalDatabaseAnalyzer()
    success = analyzer.run_full_analysis()

    if success:
        print(
            "\n🎉 Анализ завершен! Проверьте папку 'local_db_analysis' для результатов."
        )
        print("\n💡 Следующие шаги:")
        print("1. Изучите analysis_report_*.txt")
        print("2. Используйте full_analysis_*.json для программной обработки")
        print("3. Примените рекомендации для улучшения веб-интерфейса")
    else:
        print("\n❌ Анализ не удался. Проверьте подключение к удаленной базе данных.")

    return success


if __name__ == "__main__":
    main()
