# PowerShell script to install all dependencies
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installing Dependencies" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = $PSScriptRoot
$errors = @()

# Install Backend Dependencies
Write-Host "Installing Backend Dependencies (Python)..." -ForegroundColor Green
$backendDir = Join-Path $scriptPath "backend-simulation"
if (Test-Path $backendDir) {
    Set-Location $backendDir
    try {
        python -m pip install -r requirements.txt
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Backend dependencies installed successfully" -ForegroundColor Green
        } else {
            $errors += "Backend installation failed"
            Write-Host "✗ Backend installation failed" -ForegroundColor Red
        }
    } catch {
        $errors += "Backend installation error: $_"
        Write-Host "✗ Backend installation error: $_" -ForegroundColor Red
    }
} else {
    $errors += "Backend directory not found"
    Write-Host "✗ Backend directory not found" -ForegroundColor Red
}

Write-Host ""

# Install Frontend Dependencies
Write-Host "Installing Frontend Dependencies (Node.js)..." -ForegroundColor Green
$frontendDir = Join-Path $scriptPath "web-platform"
if (Test-Path $frontendDir) {
    Set-Location $frontendDir
    try {
        npm install
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Frontend dependencies installed successfully" -ForegroundColor Green
        } else {
            $errors += "Frontend installation failed"
            Write-Host "✗ Frontend installation failed" -ForegroundColor Red
        }
    } catch {
        $errors += "Frontend installation error: $_"
        Write-Host "✗ Frontend installation error: $_" -ForegroundColor Red
    }
} else {
    $errors += "Frontend directory not found"
    Write-Host "✗ Frontend directory not found" -ForegroundColor Red
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($errors.Count -eq 0) {
    Write-Host "✓ All dependencies installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  - Run .\start-all.ps1 to start both servers" -ForegroundColor Cyan
    Write-Host "  - Or run .\start-backend.ps1 and .\start-frontend.ps1 separately" -ForegroundColor Cyan
} else {
    Write-Host "✗ Some errors occurred during installation:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $error" -ForegroundColor Red
    }
    exit 1
}

Set-Location $scriptPath
