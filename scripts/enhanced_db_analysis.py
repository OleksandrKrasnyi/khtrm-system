#!/usr/bin/env python3
"""
Enhanced Database Analysis Tool
Анализ структуры базы данных диспетчера для улучшения веб-интерфейса
"""

import json
import os
from datetime import datetime
from typing import Any

import mysql.connector
from mysql.connector import Error


class DatabaseAnalyzer:
    """Класс для анализа структуры базы данных диспетчера"""

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
        }
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        """Подключение к базе данных"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("✅ Успешное подключение к базе данных")
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

    def get_table_structure(self, table_name: str) -> dict[str, Any]:
        """Получение структуры таблицы"""
        try:
            # Получение структуры таблицы
            self.cursor.execute(f"DESCRIBE {table_name}")
            structure = self.cursor.fetchall()

            # Получение подробной информации о столбцах
            self.cursor.execute(f"""
                SELECT
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    COLUMN_TYPE,
                    COLUMN_COMMENT
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = '{self.config["database"]}'
                AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
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

    def get_field_values(
        self, table_name: str, field_name: str, limit: int = 20
    ) -> list[dict[str, Any]]:
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

    def get_sample_data(
        self, table_name: str, date_filter: str = None, limit: int = 10
    ) -> list[dict[str, Any]]:
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

    def analyze_zanaradka_table(self) -> dict[str, Any]:
        """Полный анализ таблицы zanaradka"""
        print("📊 Анализ таблицы zanaradka...")

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
            self.cursor.execute("""
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
            """)
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

    def analyze_related_tables(self) -> dict[str, Any]:
        """Анализ связанных таблиц"""
        print("📊 Анализ связанных таблиц...")

        related_tables = ["sprmarshrut", "sprpersonal", "sprpe"]
        analysis = {}

        for table in related_tables:
            print(f"   Анализ таблицы: {table}")
            try:
                structure = self.get_table_structure(table)
                sample_data = self.get_sample_data(table, limit=5)

                analysis[table] = {"structure": structure, "sample_data": sample_data}
            except Error as e:
                print(f"❌ Ошибка анализа таблицы {table}: {e}")
                analysis[table] = {"error": str(e)}

        return analysis

    def create_field_mapping(self) -> dict[str, Any]:
        """Создание карты полей между БД и веб-интерфейсом"""
        print("📊 Создание карты полей...")

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

    def generate_improvement_recommendations(
        self, analysis_data: dict[str, Any]
    ) -> list[str]:
        """Генерация рекомендаций по улучшению"""
        recommendations = []

        # Проблемы с Simple View
        recommendations.append(
            "🔧 Simple View: Показывает только ФИО водителя, должно быть больше полей"
        )
        recommendations.append(
            "📝 Simple View: Добавить маршрут, смену, номер ПС, времена выхода/захода"
        )

        # Проблемы с маппингом полей
        recommendations.append(
            "🔧 Backend: Исправить неправильное поле 'putlist???' на 'pe№' для номера ПС"
        )
        recommendations.append(
            "🔧 Backend: Исправить неправильное поле 'putlist???' на 'putlist№' для путевого листа"
        )

        # Проблемы с кодировкой
        recommendations.append(
            "🔧 Encoding: Улучшить обработку украинских символов в именах"
        )

        # Проблемы с Extended View
        recommendations.append(
            "📝 Extended View: Добавить недостающие поля согласно анализу БД"
        )

        # Проблемы с Full View
        recommendations.append(
            "📝 Full View: Привести в соответствие с оригинальной структурой MS Access"
        )

        return recommendations

    def save_analysis_results(
        self, analysis_data: dict[str, Any], output_dir: str = "python_db_analysis"
    ):
        """Сохранение результатов анализа"""
        print(f"💾 Сохранение результатов в папку: {output_dir}")

        # Создание папки для результатов
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Сохранение в JSON для программной обработки
        with open(
            os.path.join(output_dir, "full_analysis.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2, default=str)

        # Сохранение читаемого отчета
        with open(
            os.path.join(output_dir, "analysis_report.txt"), "w", encoding="utf-8"
        ) as f:
            f.write("=== АНАЛИЗ БАЗЫ ДАННЫХ ДИСПЕТЧЕРА ===\n")
            f.write(f"Дата анализа: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
            f.write("Инструмент: Python Database Analyzer\n\n")

            # Структура таблицы zanaradka
            f.write("=== СТРУКТУРА ТАБЛИЦЫ ZANARADKA ===\n")
            zanaradka_data = analysis_data.get("zanaradka_analysis", {})
            structure = zanaradka_data.get("structure", {})

            if structure.get("detailed_structure"):
                f.write(f"Количество записей: {structure.get('row_count', 0)}\n")
                f.write("Поля таблицы:\n")
                for field in structure["detailed_structure"]:
                    f.write(
                        f"  {field['COLUMN_NAME']}: {field['COLUMN_TYPE']} ({field['DATA_TYPE']})\n"
                    )
                f.write("\n")

            # Анализ полей
            f.write("=== АНАЛИЗ ЗНАЧЕНИЙ ПОЛЕЙ ===\n")
            field_analysis = zanaradka_data.get("field_analysis", {})
            for field_name, values in field_analysis.items():
                f.write(f"\n{field_name.upper()}:\n")
                for value_info in values[:10]:  # Top 10 values
                    f.write(f"  {value_info['value']}: {value_info['count']} раз\n")

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
        print("🚀 Запуск полного анализа базы данных диспетчера...")
        print("=" * 60)

        if not self.connect():
            return False

        try:
            # Анализ основной таблицы
            zanaradka_analysis = self.analyze_zanaradka_table()

            # Анализ связанных таблиц
            related_tables_analysis = self.analyze_related_tables()

            # Создание карты полей
            field_mapping = self.create_field_mapping()

            # Сборка всех результатов
            full_analysis = {
                "timestamp": datetime.now().isoformat(),
                "database_info": {
                    "host": self.config["host"],
                    "database": self.config["database"],
                    "connection_status": "success",
                },
                "zanaradka_analysis": zanaradka_analysis,
                "related_tables_analysis": related_tables_analysis,
                "field_mapping": field_mapping,
                "recommendations": self.generate_improvement_recommendations(
                    zanaradka_analysis
                ),
            }

            # Сохранение результатов
            self.save_analysis_results(full_analysis)

            print("=" * 60)
            print("✅ Анализ завершен успешно!")
            print("📁 Результаты сохранены в папке 'python_db_analysis'")
            print("📊 Основные находки:")
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
    print("🔍 Enhanced Database Analysis Tool")
    print("Инструмент для анализа базы данных диспетчера")
    print("=" * 60)

    # Проверка зависимостей
    try:
        import importlib.util

        if importlib.util.find_spec("mysql.connector") is None:
            raise ImportError("mysql-connector-python not found")
    except ImportError:
        print("❌ Ошибка: Не найден модуль mysql-connector-python")
        print("Установите его командой: pip install mysql-connector-python")
        return False

    # Запуск анализа
    analyzer = DatabaseAnalyzer()
    success = analyzer.run_full_analysis()

    if success:
        print(
            "\n🎉 Анализ завершен! Проверьте папку 'python_db_analysis' для результатов."
        )
    else:
        print("\n❌ Анализ не удался. Проверьте подключение к базе данных.")

    return success


if __name__ == "__main__":
    main()
