import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def import_package(package):
    exec(f'import {package}')

def install_package_if_not_already(package):
    try:
        import_package(package)
    except:
        install(package)
        print(f"Package {package} installed succesfully.")


packages = ['numpy', 'matplotlib', 'pandas', 'tqdm', 'chess', 'svglib', 'reportlab', 'pickle', 'glob', 
'tkinter', 'customtkinter', 'Pillow']

for package in packages:
    install_package_if_not_already(package)


