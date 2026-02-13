# PowerShell script to start both backend and frontend servers
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Telecom Fraud ML - Starting Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = $PSScriptRoot

# Start backend in a new window
Write-Host "Starting Backend Server in new window..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", (Join-Path $scriptPath "start-backend.ps1")

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in a new window
Write-Host "Starting Frontend Server in new window..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-File", (Join-Path $scriptPath "start-frontend.ps1")

Write-Host ""
Write-Host "Both servers are starting in separate windows." -ForegroundColor Cyan
Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this script (servers will continue running)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
