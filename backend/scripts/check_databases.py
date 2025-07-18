#!/usr/bin/env python3
"""
Check available databases for user khtrm_remote
"""

import os

import pymysql

# Connection settings
MYSQL_CONFIG = {
    "host": "91.222.248.216",
    "port": 61315,
    "user": "khtrm_remote",
    "password": os.getenv("MYSQL_PASSWORD", "your_password_here"),
    "charset": "utf8mb4",
    "connect_timeout": 10,
}


def check_available_databases() -> None:
    """Check available databases"""
    print("🔍 Checking available databases for user khtrm_remote")
    print("=" * 60)

    try:
        # Connection without specifying specific database
        connection = pymysql.connect(**MYSQL_CONFIG)
        cursor = connection.cursor()

        # Show all databases
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        print(f"📋 Found databases: {len(databases)}")
        for db in databases:
            print(f"   - {db[0]}")

        print("\n🔍 Checking access to specific databases:")

        # Check access to various databases
        test_databases = [
            "saltdepoavt_",
            "trd2depoavt",
            "saltdepoavt",
            "information_schema",
            "mysql",
            "performance_schema",
        ]

        for db_name in test_databases:
            try:
                cursor.execute(f"USE {db_name}")
                cursor.execute(
                    "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s",
                    (db_name,),
                )
                table_count = cursor.fetchone()[0]
                print(f"   ✅ {db_name} - accessible, tables: {table_count}")
            except Exception as e:
                print(f"   ❌ {db_name} - not accessible: {e}")

        # Check user privileges
        print("\n🔐 User privileges:")
        cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
        grants = cursor.fetchall()

        for grant in grants:
            print(f"   - {grant[0]}")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"❌ Connection error: {e}")


def suggest_solutions() -> None:
    """Suggest solutions"""
    print("\n🔧 Possible solutions:")
    print("1. Ask admin to grant privileges on saltdepoavt_ database:")
    print("   GRANT ALL PRIVILEGES ON saltdepoavt_.* TO 'khtrm_remote'@'%';")
    print("   FLUSH PRIVILEGES;")
    print()
    print("2. Create saltdepoavt_ database if it doesn't exist:")
    print("   CREATE DATABASE saltdepoavt_;")
    print()
    print("3. Verify correct database name")
    print()
    print("4. Use trd2depoavt database (if available)")


if __name__ == "__main__":
    check_available_databases()
    suggest_solutions()
