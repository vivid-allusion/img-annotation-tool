#!/usr/bin/env python3
"""Bootstrap script - installs dependencies and runs the main entry point."""

import subprocess
import sys
from pathlib import Path

VENV_DIR = Path(".venv")
REQUIREMENTS = Path("requirements.txt")
MAIN_ENTRY = Path("src/main.py")


def get_python() -> Path:
    """Get the Python executable path in the venv."""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def create_venv() -> None:
    """Create virtual environment if it doesn't exist."""
    if VENV_DIR.exists():
        return
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)


def install_dependencies() -> None:
    """Install dependencies from requirements.txt."""
    if not REQUIREMENTS.exists():
        print(f"Error: {REQUIREMENTS} not found")
        sys.exit(1)
    print("Installing dependencies...")
    subprocess.run([str(get_python()), "-m", "pip", "install", "-r", str(REQUIREMENTS)], check=True)


def run_main() -> None:
    """Run the main entry point."""
    if not MAIN_ENTRY.exists():
        print(f"Error: {MAIN_ENTRY} not found")
        sys.exit(1)
    subprocess.run([str(get_python()), str(MAIN_ENTRY)], check=False)


def main() -> None:
    """Bootstrap and run the application."""
    create_venv()
    install_dependencies()
    run_main()


if __name__ == "__main__":
    main()
