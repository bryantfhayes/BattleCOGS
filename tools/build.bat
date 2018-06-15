PyInstaller main.py --onefile --paths=.\lib --hidden-import=_cffi_backend
echo d | xcopy assets dist\assets /S/H/E
