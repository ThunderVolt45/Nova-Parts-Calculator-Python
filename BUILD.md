# Build

This project is a PyQt6 desktop app. The entry point is `calculator.py`.

## Run from source

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe calculator.py
```

## Build Windows exe

```powershell
.\build.ps1
```

The executable is created at:

```text
dist\NovaPartsCalculator.exe
```

The PyInstaller command includes the `.ui` files and the `JSON` data directory.

Do not run or distribute files from the `build` directory. That directory contains
temporary PyInstaller files, and the exe inside it can fail with missing DLL errors.
Use `dist\NovaPartsCalculator.exe` instead.
