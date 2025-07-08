#!/usr/bin/env python3
"""
Скрипт для автоматического исправления проблем Python кода
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Запуск команды с выводом результата"""
    print(f"\n🔧 {description}")
    print("=" * 60)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"❌ Ошибка выполнения команды: {e}")
        return False


def main():
    """Основная функция исправления"""
    print("🔧 АВТОМАТИЧЕСКОЕ ИСПРАВЛЕНИЕ PYTHON КОДА")
    print("=" * 60)

    # Проверяем, что мы в корневой папке проекта
    if not os.path.exists("pyproject.toml"):
        print(
            "❌ Не найден pyproject.toml. Запустите скрипт из корневой папки проекта."
        )
        sys.exit(1)

    # Статистика до исправления
    print("\n📊 СТАТИСТИКА ДО ИСПРАВЛЕНИЯ:")
    run_command("uv run ruff check --statistics", "Текущие проблемы")

    # 1. Ruff - автоматические исправления
    print("\n🛠️  1. RUFF - АВТОМАТИЧЕСКИЕ ИСПРАВЛЕНИЯ")
    run_command("uv run ruff check --fix", "Применение базовых исправлений")

    # 2. Ruff - небезопасные исправления
    print("\n⚠️  2. RUFF - НЕБЕЗОПАСНЫЕ ИСПРАВЛЕНИЯ")
    run_command(
        "uv run ruff check --unsafe-fixes --fix", "Применение небезопасных исправлений"
    )

    # 3. Ruff - форматирование
    print("\n🎨 3. RUFF - ФОРМАТИРОВАНИЕ")
    run_command("uv run ruff format", "Форматирование кода")

    # Статистика после исправления
    print("\n📊 СТАТИСТИКА ПОСЛЕ ИСПРАВЛЕНИЯ:")
    final_success = run_command("uv run ruff check --statistics", "Оставшиеся проблемы")

    # Итоговый результат
    print("\n" + "=" * 60)
    if final_success:
        print("🎉 ВСЕ ПРОБЛЕМЫ ИСПРАВЛЕНЫ!")
        print("✅ Код готов к коммиту")
    else:
        print("⚠️  ОСТАЛИСЬ ПРОБЛЕМЫ")
        print("🔍 Некоторые проблемы требуют ручного исправления")
        print("📋 Запустите 'python scripts/python-check.py' для подробной информации")

    return 0 if final_success else 1


if __name__ == "__main__":
    sys.exit(main())
