# PowerShell script to start the backend server
Write-Host "Starting Backend Server..." -ForegroundColor Green
Write-Host ""

$backendDir = Join-Path $PSScriptRoot "backend-simulation"

if (-not (Test-Path $backendDir)) {
    Write-Host "Error: backend-simulation directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $backendDir

# Check if port 8000 is already in use
$portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "Warning: Port 8000 is already in use!" -ForegroundColor Yellow
    Write-Host "Killing existing process on port 8000..." -ForegroundColor Yellow
    $process = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($process) {
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Python is not installed or not in PATH!" -ForegroundColor Red
    exit 1
}

# Install dependencies if needed
Write-Host "Checking dependencies..." -ForegroundColor Cyan
python -m pip install -q -r requirements.txt

# Start the server
Write-Host ""
Write-Host "Starting FastAPI server on http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python main.py
