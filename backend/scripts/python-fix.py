#!/usr/bin/env python3
"""
Script for automatic Python code fixes
"""

import os
import subprocess
import sys


def run_command(cmd: str, description: str) -> bool:
    """Run command and display output"""
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
        print(f"❌ Command execution error: {e}")
        return False


def main() -> None:
    """Main fix function"""
    print("🔧 AUTOMATIC PYTHON CODE FIXES")
    print("=" * 60)

    # Check if we're in the project root
    if not os.path.exists("pyproject.toml"):
        print("❌ pyproject.toml not found. Run the script from the project root.")
        sys.exit(1)

    # Statistics before fixes
    print("\n📊 STATISTICS BEFORE FIXES:")
    run_command("uv run ruff check --statistics", "Current issues")

    # 1. Ruff - automatic fixes
    print("\n🛠️  1. RUFF - AUTOMATIC FIXES")
    run_command("uv run ruff check --fix", "Applying basic fixes")

    # 2. Ruff - unsafe fixes
    print("\n⚠️  2. RUFF - UNSAFE FIXES")
    run_command("uv run ruff check --unsafe-fixes --fix", "Applying unsafe fixes")

    # 3. Ruff - formatting
    print("\n🎨 3. RUFF - FORMATTING")
    run_command("uv run ruff format", "Code formatting")

    # Statistics after fixes
    print("\n📊 STATISTICS AFTER FIXES:")
    final_success = run_command("uv run ruff check --statistics", "Remaining issues")

    # Final result
    print("\n" + "=" * 60)
    if final_success:
        print("🎉 ALL ISSUES FIXED!")
        print("✅ Code is ready for production")
    else:
        print("⚠️  SOME ISSUES REMAIN")
        print("🔍 Some issues require manual fixing")

    print("\n🚀 Use 'uv run ruff check --fix' to apply fixes")
    print("📖 Use 'uv run ruff check --statistics' to view detailed statistics")


if __name__ == "__main__":
    main()
