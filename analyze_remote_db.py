#!/usr/bin/env python3
"""
Анализ структуры удаленной базы данных saltdepoavt_
для поиска полей "П. від" и "К. від"
"""

import json
import os
from datetime import datetime

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


def analyze_remote_database() -> None:
    """Анализ удаленной базы данных"""

    # Загрузка переменных из .env файла
    load_dotenv()

    # Настройки подключения из .env
    mysql_port = os.getenv("MYSQL_PORT", "3306")
    config = {
        "host": os.getenv("MYSQL_HOST"),
        "port": int(mysql_port),
        "database": os.getenv("MYSQL_DATABASE"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "charset": "utf8mb4",
        "use_unicode": True,
        "autocommit": True,
    }

    # Проверка наличия всех необходимых переменных
    required_vars = ["MYSQL_HOST", "MYSQL_USER", "MYSQL_PASSWORD", "MYSQL_DATABASE"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"❌ Отсутствуют переменные окружения в .env: {', '.join(missing_vars)}")
        return

    print(f"🔗 Подключение к: {config['host']}:{config['port']}/{config['database']}")
    print(f"👤 Пользователь: {config['user']}")

    print("🔍 Анализ структуры удаленной базы данных saltdepoavt_")
    print("=" * 60)

    try:
        # Подключение к базе данных
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # 1. Получить список всех таблиц
        print("📋 Список таблиц в базе данных:")
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]

        for i, table in enumerate(tables, 1):
            print(f"{i:2d}. {table}")

        print(f"\nВсего таблиц: {len(tables)}")
        print("=" * 60)

        # 2. Найти таблицы с полями времени/расписания
        relevant_tables = []
        time_fields = ["time", "trab", "norma", "plan", "profit", "vih", "zah"]

        print("🕐 Поиск таблиц с полями времени:")

        for table in tables:
            try:
                cursor.execute(f"DESCRIBE {table}")
                fields = cursor.fetchall()

                # Проверить есть ли поля времени
                time_related_fields = []
                for field in fields:
                    field_name = str(field[0]).lower()
                    if any(keyword in field_name for keyword in time_fields):
                        time_related_fields.append(field[0])

                if time_related_fields:
                    relevant_tables.append(
                        {
                            "table": table,
                            "time_fields": time_related_fields,
                            "total_fields": len(fields),
                        }
                    )
                    print(
                        f"  ✓ {table}: {', '.join(time_related_fields[:5])}{'...' if len(time_related_fields) > 5 else ''}"
                    )

            except Error as e:
                print(f"  ✗ Ошибка при анализе {table}: {e}")

        print("=" * 60)

        # 3. Детальный анализ relevантных таблиц
        print("📊 Детальный анализ релевантных таблиц:")

        analysis_results = {}

        for table_info in relevant_tables[:5]:  # Ограничим 5 таблицами
            table = table_info["table"]
            print(f"\n🔎 Таблица: {table}")

            try:
                # Структура таблицы
                cursor.execute(f"DESCRIBE {table}")
                fields = cursor.fetchall()

                print(f"  Полей: {len(fields)}")

                # Показать поля с ключевыми словами
                profit_fields = []
                time_fields = []

                for field in fields:
                    field_name = str(field[0])
                    field_type = str(field[1])

                    if any(
                        keyword in field_name.lower()
                        for keyword in ["profit", "trab", "norma"]
                    ):
                        profit_fields.append(f"{field_name} ({field_type})")
                    elif any(
                        keyword in field_name.lower()
                        for keyword in ["time", "vih", "zah", "pods", "zakls"]
                    ):
                        time_fields.append(f"{field_name} ({field_type})")

                if profit_fields:
                    print(f"  💰 Поля прибыльности: {', '.join(profit_fields)}")
                if time_fields:
                    print(
                        f"  ⏰ Поля времени: {', '.join(time_fields[:10])}{'...' if len(time_fields) > 10 else ''}"
                    )

                # Примеры данных
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                sample_data = cursor.fetchall()

                if sample_data:
                    print(f"  📄 Примеры данных ({len(sample_data)} записей):")
                    column_names = [desc[0] for desc in cursor.description]

                    for i, row in enumerate(sample_data):
                        print(f"    Запись {i + 1}:")
                        for j, value in enumerate(row):
                            if j < 10:  # Показать только первые 10 полей
                                print(f"      {column_names[j]}: {value}")
                        if len(row) > 10:
                            print(f"      ... (еще {len(row) - 10} полей)")

                analysis_results[table] = {
                    "fields_count": len(fields),
                    "profit_fields": profit_fields,
                    "time_fields": time_fields,
                    "sample_count": len(sample_data),
                }

            except Error as e:
                print(f"  ✗ Ошибка при анализе {table}: {e}")

        print("=" * 60)

        # 4. Специальный поиск данных для 2025-07-07
        print("🎯 Поиск данных на 2025-07-07 в основных таблицах:")

        main_tables = ["zanaradka", "tabel", "tabel_plan_norma", "tabel_plan"]

        for table in main_tables:
            if table in tables:
                try:
                    # Проверить есть ли данные на эту дату
                    date_fields = ["data_day", "date", "data"]
                    date_field = None

                    cursor.execute(f"DESCRIBE {table}")
                    fields = cursor.fetchall()

                    for field in fields:
                        if str(field[0]).lower() in date_fields:
                            date_field = field[0]
                            break

                    if date_field:
                        cursor.execute(
                            f"SELECT COUNT(*) FROM {table} WHERE {date_field} = '2025-07-07'"
                        )
                        count = cursor.fetchone()[0]
                        print(f"  📅 {table}: {count} записей на 2025-07-07")

                        if count > 0:
                            # Показать примеры полей времени
                            time_fields_query = []
                            for field in fields:
                                if any(
                                    keyword in str(field[0]).lower()
                                    for keyword in [
                                        "time",
                                        "trab",
                                        "norma",
                                        "vih",
                                        "zah",
                                    ]
                                ):
                                    time_fields_query.append(field[0])

                            if time_fields_query:
                                fields_str = ", ".join(time_fields_query[:10])
                                cursor.execute(
                                    f"SELECT {fields_str} FROM {table} WHERE {date_field} = '2025-07-07' LIMIT 3"
                                )
                                sample = cursor.fetchall()

                                print(
                                    f"    Примеры полей времени: {', '.join(time_fields_query[:10])}"
                                )
                                for i, row in enumerate(sample):
                                    print(f"    Запись {i + 1}: {row}")

                except Error as e:
                    print(f"  ✗ Ошибка при проверке {table}: {e}")

        # 5. Сохранить результаты в файл
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_tables": len(tables),
            "tables_list": tables,
            "relevant_tables": relevant_tables,
            "analysis_results": analysis_results,
        }

        with open("db_analysis_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2, default=str)

        print("=" * 60)
        print("✅ Анализ завершен!")
        print("📄 Результаты сохранены в db_analysis_results.json")

    except Error as e:
        print(f"❌ Ошибка подключения к базе данных: {e}")
        print("\n🔧 Проверьте настройки подключения в начале файла:")
        print("  - host: адрес удаленного сервера")
        print("  - user: имя пользователя")
        print("  - password: пароль")
        print("  - database: saltdepoavt_")

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("🔌 Подключение к базе данных закрыто")


if __name__ == "__main__":
    analyze_remote_database()
