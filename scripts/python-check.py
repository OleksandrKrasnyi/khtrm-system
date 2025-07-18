#!/usr/bin/env python3
"""
Script for checking Python code quality
Python equivalent of frontend-check
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Run command and display output"""
    print(f"\n🔍 {description}")
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


def main():
    """Main check function"""
    print("🐍 PYTHON CODE QUALITY CHECK")
    print("=" * 60)

    # Check if we're in the project root
    if not os.path.exists("pyproject.toml"):
        print("❌ pyproject.toml not found. Run the script from the project root.")
        sys.exit(1)

    success = True

    # 1. Ruff - linting
    print("\n📋 1. RUFF LINTING")
    ruff_success = run_command("uv run ruff check", "Checking code quality with ruff")
    if not ruff_success:
        success = False
        print("❌ Code quality issues found")

        # Show statistics
        print("\n📊 Error statistics:")
        run_command("uv run ruff check --statistics", "Statistics by error type")
    else:
        print("✅ Code meets quality standards!")

    # 2. MyPy - type checking
    print("\n🔍 2. MYPY - TYPE CHECKING")
    mypy_success = run_command(
        "uv run mypy --config-file pyproject.toml backend/",
        "Type checking with mypy",
    )
    if not mypy_success:
        success = False
        print("❌ Type checking issues found")
    else:
        print("✅ Type checking passed!")

    # 3. Final result
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Code is ready for production")
    else:
        print("❌ ISSUES FOUND")
        print("🔧 Run 'python scripts/python-fix.py' to auto-fix issues")
        print("📖 Or run 'uv run ruff check --fix' manually")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
