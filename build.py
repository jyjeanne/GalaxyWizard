import poetry
from poetry.utils import subprocess

def build():
    print("Building for Linux...")
    subprocess.run(["poetry", "run", "pyinstaller", "--onefile", "GalaxyWizard.py"])

    print("Building for Windows...")
    subprocess.run(["poetry", "run", "pyinstaller", "--onefile", "--windowed", "GalaxyWizard.py"])

if __name__ == "__main__":
    build()