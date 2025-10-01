#!/usr/bin/env python
"""Build script for creating standalone GalaxyWizard executable with PyInstaller."""

import subprocess
import sys
import os


def build_exe():
    """Build standalone executable using PyInstaller."""
    print("Building GalaxyWizard standalone executable...")

    # Check if main.spec exists
    spec_file = os.path.join(os.path.dirname(__file__), "main.spec")
    if not os.path.exists(spec_file):
        print(f"Error: {spec_file} not found")
        sys.exit(1)

    # Run PyInstaller with the spec file
    try:
        result = subprocess.run(
            ["pyinstaller", "main.spec", "--clean"],
            check=True,
            capture_output=False
        )
        print("\n✅ Build completed successfully!")
        print("Executable location: dist/GalaxyWizard.exe")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ PyInstaller not found. Please install it with: poetry install")
        sys.exit(1)


if __name__ == "__main__":
    build_exe()
