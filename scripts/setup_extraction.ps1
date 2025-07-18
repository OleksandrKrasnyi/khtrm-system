# MS Access Data Extraction Setup Script
# Installs required dependencies for Windows

Write-Host "🚀 Setting up MS Access Data Extraction Environment..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version
    Write-Host "✅ pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found. Please install pip first." -ForegroundColor Red
    exit 1
}

# Install required Python packages
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Blue

$packages = @(
    "paramiko>=2.8.0",
    "openpyxl",
    "pandas"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Cyan
    pip install $package
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install $package" -ForegroundColor Red
    } else {
        Write-Host "✅ $package installed successfully" -ForegroundColor Green
    }
}

# Create output directories
Write-Host "📂 Creating output directories..." -ForegroundColor Blue
$directories = @("extracted_data", "extracted_access_data", "extracted_access_data/databases", "extracted_access_data/schemas")

foreach ($dir in $directories) {
    if (!(Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "📁 Directory already exists: $dir" -ForegroundColor Yellow
    }
}

Write-Host "`n🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host "Now you can run:" -ForegroundColor Yellow
Write-Host "  python scripts/quick_extract.py" -ForegroundColor White
Write-Host "  python scripts/extract_access_data.py" -ForegroundColor White 