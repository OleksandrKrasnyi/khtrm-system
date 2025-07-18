# KHTRM System Deployment Script for Windows Server 2022
# Требует PowerShell 5.1+ и права администратора

param(
    [string]$Action = "install",
    [switch]$Force,
    [switch]$Development
)

# Проверка прав администратора
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Этот скрипт требует прав администратора. Запустите PowerShell как администратор."
    exit 1
}

function Install-Docker {
    Write-Host "🐳 Установка Docker Desktop для Windows Server..." -ForegroundColor Green
    
    # Проверка наличия Docker
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        Write-Host "Docker уже установлен" -ForegroundColor Yellow
        return
    }
    
    # Включение Hyper-V и Containers
    Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All -NoRestart
    Enable-WindowsOptionalFeature -Online -FeatureName Containers -All -NoRestart
    
    # Скачать Docker Desktop
    $dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
    $dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"
    
    Write-Host "Скачивание Docker Desktop..." -ForegroundColor Blue
    Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller
    
    # Установка Docker Desktop
    Write-Host "Установка Docker Desktop..." -ForegroundColor Blue
    Start-Process -FilePath $dockerInstaller -ArgumentList "install", "--quiet" -Wait
    
    # Очистка
    Remove-Item $dockerInstaller -Force
    
    Write-Host "Docker Desktop установлен. Требуется перезагрузка!" -ForegroundColor Green
    Write-Host "После перезагрузки запустите: docker --version" -ForegroundColor Yellow
}

function Install-Prerequisites {
    Write-Host "📦 Установка предварительных требований..." -ForegroundColor Green
    
    # Git (если не установлен)
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Установка Git..." -ForegroundColor Blue
        $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe"
        $gitInstaller = "$env:TEMP\GitInstaller.exe"
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
        Start-Process -FilePath $gitInstaller -ArgumentList "/SILENT" -Wait
        Remove-Item $gitInstaller -Force
    }
    
    # PowerShell 7 (рекомендуется)
    if (-not (Get-Command pwsh -ErrorAction SilentlyContinue)) {
        Write-Host "Установка PowerShell 7..." -ForegroundColor Blue
        Invoke-Expression "& { $(Invoke-RestMethod https://aka.ms/install-powershell.ps1) } -UseMSI -Quiet"
    }
    
    # Docker Compose (если не включен в Docker Desktop)
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Host "Установка Docker Compose..." -ForegroundColor Blue
        $composeUrl = "https://github.com/docker/compose/releases/latest/download/docker-compose-windows-x86_64.exe"
        $composePath = "$env:ProgramFiles\Docker\Docker\resources\bin\docker-compose.exe"
        New-Item -ItemType Directory -Path (Split-Path $composePath) -Force
        Invoke-WebRequest -Uri $composeUrl -OutFile $composePath
    }
}

function Setup-Firewall {
    Write-Host "🔥 Настройка Windows Firewall..." -ForegroundColor Green
    
    # HTTP порт
    New-NetFirewallRule -DisplayName "KHTRM HTTP" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80 -ErrorAction SilentlyContinue
    
    # HTTPS порт
    New-NetFirewallRule -DisplayName "KHTRM HTTPS" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 443 -ErrorAction SilentlyContinue
    
    # Backend API порт
    New-NetFirewallRule -DisplayName "KHTRM API" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000 -ErrorAction SilentlyContinue
    
    # MySQL порт (если нужен внешний доступ)
    if ($Development) {
        New-NetFirewallRule -DisplayName "KHTRM MySQL" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 3306 -ErrorAction SilentlyContinue
    }
    
    Write-Host "Правила файрволла настроены" -ForegroundColor Green
}

function Deploy-Application {
    Write-Host "🚀 Развертывание KHTRM приложения..." -ForegroundColor Green
    
    # Проверка Docker
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Error "Docker не найден. Сначала установите Docker."
        exit 1
    }
    
    # Создание директории для приложения
    $appPath = "C:\khtrm-system"
    if (-not (Test-Path $appPath)) {
        New-Item -ItemType Directory -Path $appPath -Force
    }
    
    Set-Location $appPath
    
    # Клонирование репозитория (если нужно)
    if ($Force -or -not (Test-Path "docker-compose.yml")) {
        Write-Host "Клонирование репозитория..." -ForegroundColor Blue
        # git clone https://github.com/your-repo/khtrm-system.git .
        # Или скопируйте файлы вручную
    }
    
    # Создание директорий
    @("logs", "mysql-data", "ssl") | ForEach-Object {
        if (-not (Test-Path $_)) {
            New-Item -ItemType Directory -Path $_ -Force
        }
    }
    
    # Сборка и запуск контейнеров
    Write-Host "Сборка Docker образов..." -ForegroundColor Blue
    docker-compose build
    
    Write-Host "Запуск сервисов..." -ForegroundColor Blue
    docker-compose up -d
    
    # Ожидание запуска сервисов
    Write-Host "Ожидание запуска сервисов..." -ForegroundColor Blue
    Start-Sleep -Seconds 30
    
    # Проверка статуса
    docker-compose ps
    
    Write-Host "🎉 Приложение развернуто!" -ForegroundColor Green
    Write-Host "Frontend: http://localhost" -ForegroundColor Yellow
    Write-Host "Backend API: http://localhost:8000" -ForegroundColor Yellow
    Write-Host "MySQL: localhost:3306" -ForegroundColor Yellow
}

function Show-Status {
    Write-Host "📊 Статус KHTRM системы:" -ForegroundColor Green
    
    if (Get-Command docker -ErrorAction SilentlyContinue) {
        docker-compose ps
        Write-Host ""
        Write-Host "Логи сервисов:" -ForegroundColor Blue
        docker-compose logs --tail=10
    } else {
        Write-Host "Docker не установлен" -ForegroundColor Red
    }
}

function Stop-Application {
    Write-Host "⏹️ Остановка KHTRM приложения..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "Приложение остановлено" -ForegroundColor Green
}

function Remove-Application {
    Write-Host "🗑️ Удаление KHTRM приложения..." -ForegroundColor Red
    docker-compose down -v --remove-orphans
    docker system prune -f
    Write-Host "Приложение удалено" -ForegroundColor Green
}

# Главная логика скрипта
switch ($Action.ToLower()) {
    "install" {
        Install-Prerequisites
        Install-Docker
        Setup-Firewall
        Write-Host "Установка завершена. Перезагрузите систему и запустите 'deploy' для развертывания." -ForegroundColor Green
    }
    "deploy" {
        Deploy-Application
    }
    "status" {
        Show-Status
    }
    "stop" {
        Stop-Application
    }
    "remove" {
        Remove-Application
    }
    default {
        Write-Host "Использование: .\deploy-windows-server.ps1 -Action [install|deploy|status|stop|remove]" -ForegroundColor Yellow
        Write-Host "Флаги:" -ForegroundColor Yellow
        Write-Host "  -Force     : Принудительная переустановка" -ForegroundColor Yellow
        Write-Host "  -Development : Режим разработки (открыть дополнительные порты)" -ForegroundColor Yellow
    }
} 