# PowerShell script to start the frontend server
Write-Host "Starting Frontend Server..." -ForegroundColor Green
Write-Host ""

$frontendDir = Join-Path $PSScriptRoot "web-platform"

if (-not (Test-Path $frontendDir)) {
    Write-Host "Error: web-platform directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $frontendDir

# Check if port 3000 is already in use
$portInUse = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "Warning: Port 3000 is already in use!" -ForegroundColor Yellow
    Write-Host "Killing existing process on port 3000..." -ForegroundColor Yellow
    $process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($process) {
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2
    }
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: Node.js is not installed or not in PATH!" -ForegroundColor Red
    exit 1
}

# Check if npm is available
try {
    $npmVersion = npm --version 2>&1
    Write-Host "npm version: $npmVersion" -ForegroundColor Cyan
} catch {
    Write-Host "Error: npm is not installed or not in PATH!" -ForegroundColor Red
    exit 1
}

# Check if package.json exists in the current directory
if (-not (Test-Path "package.json")) {
    Write-Host "Error: package.json not found in web-platform directory!" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the project root." -ForegroundColor Yellow
    exit 1
}

# Install dependencies if node_modules doesn't exist
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    $installResult = npm install 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error installing dependencies!" -ForegroundColor Red
        Write-Host $installResult -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
}

# Start the development server
Write-Host ""
Write-Host "Starting Next.js development server on http://localhost:3000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

npm run dev
