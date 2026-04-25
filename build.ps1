$ErrorActionPreference = "Stop"

$pythonExe = $null
$pythonArgs = @()

if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = "py"
    $pythonArgs = @("-3")
} else {
    throw "Python was not found. Install Python 3, then run this script again."
}

function Invoke-BasePython {
    & $pythonExe @pythonArgs @args
}

$venvPython = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Invoke-BasePython -m venv .venv
}

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt
& $venvPython -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --name NovaPartsCalculator `
    --add-data "calculator.ui;." `
    --add-data "partSelector.ui;." `
    --add-data "typeSelector.ui;." `
    --add-data "JSON;JSON" `
    calculator.py

Write-Host "Built: dist\NovaPartsCalculator\NovaPartsCalculator.exe"
