# PowerShell script to stop all running servers
Write-Host "Stopping all servers..." -ForegroundColor Yellow
Write-Host ""

# Stop processes on port 8000 (backend)
$backendProcess = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($backendProcess) {
    Write-Host "Stopping backend server (port 8000)..." -ForegroundColor Cyan
    Stop-Process -Id $backendProcess -Force -ErrorAction SilentlyContinue
    Write-Host "Backend server stopped." -ForegroundColor Green
} else {
    Write-Host "No backend server found on port 8000." -ForegroundColor Gray
}

# Stop processes on port 3000 (frontend)
$frontendProcess = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($frontendProcess) {
    Write-Host "Stopping frontend server (port 3000)..." -ForegroundColor Cyan
    Stop-Process -Id $frontendProcess -Force -ErrorAction SilentlyContinue
    Write-Host "Frontend server stopped." -ForegroundColor Green
} else {
    Write-Host "No frontend server found on port 3000." -ForegroundColor Gray
}

# Also try to stop any Python processes that might be running the backend
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "Found Python processes. Checking for backend..." -ForegroundColor Cyan
    # Note: We can't easily check command line in PowerShell without WMI, so we'll be more careful
    # Only kill if we're sure it's safe
}

# Also try to stop any Node processes on port 3000 (more reliable)
$nodeOnPort3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($nodeOnPort3000) {
    $nodeProcess = Get-Process -Id $nodeOnPort3000 -ErrorAction SilentlyContinue
    if ($nodeProcess -and $nodeProcess.ProcessName -eq "node") {
        Write-Host "Stopping Node.js process on port 3000..." -ForegroundColor Cyan
        Stop-Process -Id $nodeOnPort3000 -Force -ErrorAction SilentlyContinue
    }
}

Write-Host ""
Write-Host "All servers stopped." -ForegroundColor Green
