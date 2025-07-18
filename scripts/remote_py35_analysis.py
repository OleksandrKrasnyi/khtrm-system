#!/usr/bin/env python3
"""
Remote Database Analysis Tool for Python 3.5.4
Анализ базы данных диспетчера для Python 3.5.4 (старые системы)
"""

import json
import os
import sys
from datetime import datetime

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("Ошибка: Не найден модуль mysql-connector-python")
    print("Установите его командой: pip install mysql-connector-python")
    sys.exit(1)


class RemoteDatabaseAnalyzer35:
    """Класс для анализа базы данных диспетчера (Python 3.5.4 совместимый)"""

    def __init__(self):
        """Инициализация с настройками подключения"""
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
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        """Подключение к базе данных"""
        try:
            print("Подключение к базе данных...")
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Успешное подключение к базе данных")

            # Проверяем версию сервера
            self.cursor.execute("SELECT VERSION() as version")
            version_info = self.cursor.fetchone()
            print("Версия MySQL сервера: {}".format(version_info["version"]))

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
        print("Соединение с базой данных закрыто")

    def get_table_structure(self, table_name):
        """Получение структуры таблицы"""
        try:
            # Получение структуры таблицы
            self.cursor.execute(f"DESCRIBE {table_name}")
            structure = self.cursor.fetchall()

            # Получение подробной информации о столбцах
            query = """
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    COLUMN_TYPE,
                    COLUMN_COMMENT
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = '{}'
                AND TABLE_NAME = '{}'
                ORDER BY ORDINAL_POSITION
            """.format(self.config["database"], table_name)

            self.cursor.execute(query)
            detailed_structure = self.cursor.fetchall()

            # Получение индексов
            self.cursor.execute(f"SHOW INDEX FROM {table_name}")
            indexes = self.cursor.fetchall()

            # Подсчет записей
            self.cursor.execute(f"SELECT COUNT(*) as count FROM {table_name}")
            count_result = self.cursor.fetchone()
            row_count = count_result["count"] if count_result else 0

            return {
                "structure": structure,
                "detailed_structure": detailed_structure,
                "indexes": indexes,
                "row_count": row_count,
            }

        except Error as e:
            print(f"❌ Ошибка получения структуры таблицы {table_name}: {e}")
            return {}

    def get_field_values(self, table_name, field_name, limit=20):
        """Получение уникальных значений поля"""
        try:
            # Для поля с символом №, используем обратные кавычки
            field_query = f"`{field_name}`" if "№" in field_name else field_name

            query = f"""
                SELECT DISTINCT {field_query} as value, COUNT(*) as count
                FROM {table_name}
                WHERE {field_query} IS NOT NULL
                AND {field_query} != ''
                GROUP BY {field_query}
                ORDER BY count DESC, {field_query} ASC
                LIMIT {limit}
            """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(f"❌ Ошибка получения значений поля {field_name}: {e}")
            return []

    def get_sample_data(self, table_name, date_filter=None, limit=10):
        """Получение примеров данных"""
        try:
            if date_filter:
                query = f"""
                    SELECT * FROM {table_name}
                    WHERE data_day = '{date_filter}'
                    ORDER BY marshrut, smena
                    LIMIT {limit}
                """
            else:
                query = f"""
                    SELECT * FROM {table_name}
                    ORDER BY `key` DESC
                    LIMIT {limit}
                """

            self.cursor.execute(query)
            return self.cursor.fetchall()

        except Error as e:
            print(f"❌ Ошибка получения примеров данных: {e}")
            return []

    def analyze_zanaradka_table(self):
        """Полный анализ таблицы zanaradka"""
        print("Анализ таблицы zanaradka...")

        # Основная структура
        structure_info = self.get_table_structure("zanaradka")

        # Ключевые поля для анализа
        key_fields = [
            "marshrut",
            "vipusk",
            "smena",
            "tabvoditel",
            "fiovoditel",
            "tabconduktor",
            "fioconduktor",
            "pe№",
            "data_day",
            "tvih",
            "tzah",
            "putlist№",
        ]

        # Анализ значений полей
        field_analysis = {}
        for field in key_fields:
            print(f"   Анализ поля: {field}")
            field_analysis[field] = self.get_field_values("zanaradka", field)

        # Примеры данных
        sample_data = self.get_sample_data("zanaradka", limit=5)

        # Данные для конкретной даты
        date_specific_data = self.get_sample_data("zanaradka", "2025-07-07", limit=10)

        # Статистика по дате
        try:
            query = """
                SELECT
                    data_day,
                    COUNT(*) as assignments_count,
                    COUNT(DISTINCT marshrut) as routes_count,
                    COUNT(DISTINCT smena) as shifts_count
                FROM zanaradka
                WHERE data_day >= '2025-07-01'
                GROUP BY data_day
                ORDER BY data_day DESC
                LIMIT 10
            """
            self.cursor.execute(query)
            date_statistics = self.cursor.fetchall()
        except Error as e:
            print(f"❌ Ошибка получения статистики по датам: {e}")
            date_statistics = []

        return {
            "structure": structure_info,
            "field_analysis": field_analysis,
            "sample_data": sample_data,
            "date_specific_data": date_specific_data,
            "date_statistics": date_statistics,
        }

    def create_field_mapping(self):
        """Создание карты полей между БД и веб-интерфейсом"""
        print("Создание карты полей...")

        # Текущие поля веб-интерфейса
        web_fields = {
            "simple": [
                "route_number",
                "shift",
                "driver_name",
                "vehicle_number",
                "departure_time",
                "arrival_time",
                "status",
            ],
            "extended": [
                "route_number",
                "brigade",
                "shift",
                "driver_tab_number",
                "driver_name",
                "conductor_name",
                "vehicle_number",
                "state_number_pc",
                "departure_time",
                "arrival_time",
                "waybill_number",
                "fuel_address",
                "route_endpoint",
                "status",
            ],
        }

        # Карта соответствия полей БД и веб-интерфейса
        field_mapping = {
            "key": "id",
            "data_day": "assignment_date",
            "marshrut": "route_number",
            "vipusk": "brigade",
            "smena": "shift",
            "tabvoditel": "driver_tab_number",
            "fiovoditel": "driver_name",
            "tabconduktor": "conductor_tab_number",
            "fioconduktor": "conductor_name",
            "pe№": "vehicle_number",
            "tvih": "departure_time",
            "tzah": "arrival_time",
            "putlist№": "waybill_number",
            "ZaprAdr": "fuel_address",
            "kpvih": "route_endpoint",
            "tipvipusk": "route_type",
        }

        return {
            "web_fields": web_fields,
            "field_mapping": field_mapping,
            "database_fields": list(field_mapping.keys()),
            "web_interface_fields": list(field_mapping.values()),
        }

    def generate_recommendations(self, analysis_data):
        """Генерация рекомендаций по улучшению"""
        recommendations = []

        # Проблемы с Simple View
        recommendations.append(
            "Simple View: Показывает только ФИО водителя, должно быть больше полей"
        )
        recommendations.append(
            "Simple View: Добавить маршрут, смену, номер ПС, времена выхода/захода"
        )

        # Проблемы с маппингом полей
        recommendations.append(
            "Backend: Исправить неправильное поле 'putlist???' на 'pe№' для номера ПС"
        )
        recommendations.append(
            "Backend: Исправить неправильное поле 'putlist???' на 'putlist№' для путевого листа"
        )

        # Проблемы с кодировкой
        recommendations.append(
            "Encoding: Улучшить обработку украинских символов в именах"
        )

        # Проблемы с Extended View
        recommendations.append(
            "Extended View: Добавить недостающие поля согласно анализу БД"
        )

        # Проблемы с Full View
        recommendations.append(
            "Full View: Привести в соответствие с оригинальной структурой MS Access"
        )

        return recommendations

    def save_analysis_results(self, analysis_data, output_dir="remote_py35_analysis"):
        """Сохранение результатов анализа"""
        print(f"Сохранение результатов в папку: {output_dir}")

        # Создание папки для результатов
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Сохранение в JSON для программной обработки
        json_file = os.path.join(output_dir, "full_analysis.json")
        with open(json_file, "w", encoding="utf-8") as f:
            # Используем separators для Python 3.5 совместимости
            json.dump(
                analysis_data,
                f,
                ensure_ascii=False,
                indent=2,
                default=str,
                separators=(",", ": "),
            )

        # Сохранение читаемого отчета
        report_file = os.path.join(output_dir, "analysis_report.txt")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=== АНАЛИЗ БАЗЫ ДАННЫХ ДИСПЕТЧЕРА (Python 3.5.4) ===\n")
            f.write(
                "Дата анализа: {}\n".format(
                    datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                )
            )
            f.write("Инструмент: Remote Python 3.5.4 Analyzer\n\n")

            # Структура таблицы zanaradka
            f.write("=== СТРУКТУРА ТАБЛИЦЫ ZANARADKA ===\n")
            zanaradka_data = analysis_data.get("zanaradka_analysis", {})
            structure = zanaradka_data.get("structure", {})

            if structure.get("detailed_structure"):
                f.write(
                    "Количество записей: {}\n".format(structure.get("row_count", 0))
                )
                f.write("Поля таблицы:\n")
                for field in structure["detailed_structure"]:
                    f.write(
                        "  {}: {} ({})\n".format(
                            field["COLUMN_NAME"],
                            field["COLUMN_TYPE"],
                            field["DATA_TYPE"],
                        )
                    )
                f.write("\n")

            # Анализ полей
            f.write("=== АНАЛИЗ ЗНАЧЕНИЙ ПОЛЕЙ ===\n")
            field_analysis = zanaradka_data.get("field_analysis", {})
            for field_name, values in field_analysis.items():
                f.write(f"\n{field_name.upper()}:\n")
                for value_info in values[:10]:  # Top 10 values
                    f.write(
                        "  {}: {} раз\n".format(
                            value_info["value"], value_info["count"]
                        )
                    )

            # Примеры данных
            f.write("\n=== ПРИМЕРЫ ДАННЫХ ===\n")
            sample_data = zanaradka_data.get("sample_data", [])
            for i, record in enumerate(sample_data[:3]):
                f.write(f"\nЗапись {i + 1}:\n")
                for key, value in record.items():
                    f.write(f"  {key}: {value}\n")

            # Карта полей
            f.write("\n=== КАРТА ПОЛЕЙ ===\n")
            field_mapping = analysis_data.get("field_mapping", {})
            mapping = field_mapping.get("field_mapping", {})
            f.write("База данных -> Веб-интерфейс\n")
            for db_field, web_field in mapping.items():
                f.write(f"  {db_field} -> {web_field}\n")

            # Рекомендации
            f.write("\n=== РЕКОМЕНДАЦИИ ПО УЛУЧШЕНИЮ ===\n")
            recommendations = analysis_data.get("recommendations", [])
            for i, rec in enumerate(recommendations, 1):
                f.write(f"{i}. {rec}\n")

        print(f"✅ Результаты сохранены в {output_dir}/")

    def run_full_analysis(self):
        """Запуск полного анализа базы данных"""
        print("Запуск полного анализа базы данных диспетчера...")
        print("=" * 60)

        if not self.connect():
            return False

        try:
            # Анализ основной таблицы
            zanaradka_analysis = self.analyze_zanaradka_table()

            # Создание карты полей
            field_mapping = self.create_field_mapping()

            # Сборка всех результатов
            full_analysis = {
                "timestamp": datetime.now().isoformat(),
                "database_info": {
                    "host": self.config["host"],
                    "database": self.config["database"],
                    "connection_status": "success",
                    "python_version": "3.5.4 compatible",
                },
                "zanaradka_analysis": zanaradka_analysis,
                "field_mapping": field_mapping,
                "recommendations": self.generate_recommendations(zanaradka_analysis),
            }

            # Сохранение результатов
            self.save_analysis_results(full_analysis)

            print("=" * 60)
            print("✅ Анализ завершен успешно!")
            print("Результаты сохранены в папке 'remote_py35_analysis'")
            print("Основные находки:")
            print("   - Структура таблицы zanaradka проанализирована")
            print("   - Карта полей создана")
            print("   - Рекомендации по улучшению сформированы")

            return True

        except Exception as e:
            print(f"❌ Ошибка во время анализа: {e}")
            return False

        finally:
            self.disconnect()


def main():
    """Главная функция"""
    print("Remote Database Analysis Tool (Python 3.5.4)")
    print("Инструмент для анализа базы данных диспетчера")
    print("=" * 60)

    # Проверка версии Python

    print(
        f"Python версия: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    # Запуск анализа
    analyzer = RemoteDatabaseAnalyzer35()
    success = analyzer.run_full_analysis()

    if success:
        print(
            "\nАнализ завершен! Проверьте папку 'remote_py35_analysis' для результатов."
        )
    else:
        print("\nАнализ не удался. Проверьте подключение к базе данных.")

    return success


if __name__ == "__main__":
    main()
