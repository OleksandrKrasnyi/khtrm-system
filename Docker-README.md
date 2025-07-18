# KHTRM System - Docker Deployment Guide

## 🐳 Развертывание через Docker на Windows Server 2022

### Преимущества Docker подхода:
- ✅ **Простота установки** - один скрипт устанавливает все
- ✅ **Изолированность** - каждый сервис в своем контейнере
- ✅ **Масштабируемость** - легко добавлять новые сервисы
- ✅ **Консистентность** - одинаковое поведение в dev/staging/prod
- ✅ **Быстрое развертывание** - 5-10 минут до запуска

---

## 📋 Требования

### Системные требования:
- **Windows Server 2022** (или Windows 10/11 Pro)
- **RAM**: минимум 4GB, рекомендуется 8GB+
- **Диск**: минимум 10GB свободного места
- **Права администратора**

### Порты:
- **80** - Frontend (HTTP)
- **443** - Frontend (HTTPS)
- **8000** - Backend API
- **3306** - MySQL (опционально, для внешнего доступа)

---

## 🚀 Быстрый старт

### 1. Автоматическая установка (рекомендуется)

```powershell
# Запустить PowerShell от имени администратора
# Скачать и запустить скрипт установки
.\deploy-windows-server.ps1 -Action install
```

### 2. Перезагрузка системы
```powershell
Restart-Computer
```

### 3. Развертывание приложения
```powershell
# После перезагрузки
.\deploy-windows-server.ps1 -Action deploy
```

### 4. Проверка статуса
```powershell
.\deploy-windows-server.ps1 -Action status
```

---

## 🔧 Ручная установка

### Шаг 1: Установить Docker Desktop

```powershell
# Включить Hyper-V и контейнеры
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All -NoRestart
Enable-WindowsOptionalFeature -Online -FeatureName Containers -All -NoRestart

# Скачать и установить Docker Desktop
$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
Invoke-WebRequest -Uri $dockerUrl -OutFile "DockerInstaller.exe"
Start-Process -FilePath "DockerInstaller.exe" -ArgumentList "install", "--quiet" -Wait

# Перезагрузить систему
Restart-Computer
```

### Шаг 2: Настроить файрволл

```powershell
# HTTP/HTTPS порты
New-NetFirewallRule -DisplayName "KHTRM HTTP" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 80
New-NetFirewallRule -DisplayName "KHTRM HTTPS" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 443
New-NetFirewallRule -DisplayName "KHTRM API" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 8000
```

### Шаг 3: Клонировать репозиторий

```powershell
# Создать директорию для приложения
New-Item -ItemType Directory -Path "C:\khtrm-system" -Force
Set-Location "C:\khtrm-system"

# Клонировать репозиторий
git clone https://github.com/your-repo/khtrm-system.git .
```

### Шаг 4: Запустить приложение

```powershell
# Сборка контейнеров
docker-compose build

# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

---

## 📊 Архитектура контейнеров

```
┌─────────────────────────────────────────────────────────────┐
│                    KHTRM System                             │
├─────────────────────────────────────────────────────────────┤
│  Frontend (nginx)     │  Backend (FastAPI)   │  Database   │
│  Port: 80, 443        │  Port: 8000          │  MySQL 8.0  │
│  Vue.js SPA           │  Python 3.12         │  Port: 3306 │
├─────────────────────────────────────────────────────────────┤
│                 Docker Network: khtrm-network               │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Мониторинг и управление

### Просмотр логов
```powershell
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
```

### Перезапуск сервисов
```powershell
# Перезапустить все
docker-compose restart

# Перезапустить конкретный сервис
docker-compose restart backend
```

### Остановка и запуск
```powershell
# Остановить все
docker-compose down

# Запустить все
docker-compose up -d
```

### Обновление приложения
```powershell
# Остановить контейнеры
docker-compose down

# Обновить код
git pull

# Пересобрать и запустить
docker-compose build
docker-compose up -d
```

---

## 🛠️ Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Database Configuration
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=trd2depoavt
MYSQL_USER=khtrm_remote
MYSQL_PASSWORD=KhTRM_2025!

# Application Configuration
DEBUG=False
DATABASE_ECHO=False
SECRET_KEY=your-super-secret-key-here

# Network Configuration
FRONTEND_PORT=80
BACKEND_PORT=8000
MYSQL_PORT=3306
```

### Кастомизация портов

Отредактируйте `docker-compose.yml` для изменения портов:

```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Изменить с 80 на 8080
  
  backend:
    ports:
      - "8001:8000"  # Изменить с 8000 на 8001
```

---

## 🔐 Безопасность

### SSL/TLS сертификаты

```powershell
# Создать директорию для сертификатов
New-Item -ItemType Directory -Path "ssl" -Force

# Поместить сертификаты в папку ssl/
# ssl/cert.pem
# ssl/key.pem
```

### Backup базы данных

```powershell
# Создать backup
docker-compose exec mysql mysqldump -u root -p trd2depoavt > backup.sql

# Восстановить backup
docker-compose exec -i mysql mysql -u root -p trd2depoavt < backup.sql
```

---

## 🚨 Устранение проблем

### Docker не запускается
```powershell
# Проверить статус Docker
Get-Service docker
Get-Process docker

# Перезапустить Docker
Restart-Service docker
```

### Контейнер не запускается
```powershell
# Просмотреть логи
docker-compose logs service_name

# Проверить конфигурацию
docker-compose config
```

### Проблемы с портами
```powershell
# Проверить занятые порты
netstat -an | findstr :80
netstat -an | findstr :8000
netstat -an | findstr :3306
```

### Очистка Docker
```powershell
# Удалить неиспользуемые контейнеры
docker system prune -f

# Удалить все контейнеры и образы
docker system prune -a -f
```

---

## 📞 Поддержка

### Полезные команды

```powershell
# Статус всех контейнеров
docker-compose ps

# Использование ресурсов
docker stats

# Информация о системе
docker system info

# Версии
docker --version
docker-compose --version
```

### Контакты

- **Разработчик**: [Ваше имя]
- **Email**: [your-email@example.com]
- **GitHub**: [https://github.com/your-repo]

---

## 🎯 Следующие шаги

1. **Мониторинг**: Настроить мониторинг с помощью Grafana + Prometheus
2. **CI/CD**: Настроить автоматическое развертывание
3. **Масштабирование**: Добавить load balancer для multiple instances
4. **Резервное копирование**: Автоматические backups базы данных

---

**🎉 Готово! Ваше приложение KHTRM работает в Docker контейнерах!**

**Адреса после развертывания:**
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **MySQL**: localhost:3306 