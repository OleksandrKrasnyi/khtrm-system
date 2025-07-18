# 🚀 KHTRM System - Быстрый старт с Docker

## 💻 Установка на Windows Server 2022

### ⚡ Автоматическая установка (5 минут)

1. **Скачайте проект**
2. **Запустите PowerShell от имени администратора**
3. **Выполните установку:**

```powershell
# Установка Docker и зависимостей
.\deploy-windows-server.ps1 -Action install

# Перезагрузка системы
Restart-Computer

# Развертывание приложения
.\deploy-windows-server.ps1 -Action deploy
```

## 🌐 Доступ к приложению

После развертывания:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:8000
- **MySQL**: localhost:3306

## 🔧 Управление

```powershell
# Проверить статус
.\deploy-windows-server.ps1 -Action status

# Остановить приложение
.\deploy-windows-server.ps1 -Action stop

# Удалить приложение
.\deploy-windows-server.ps1 -Action remove
```

## 📊 Мониторинг

```powershell
# Просмотр логов
docker-compose logs

# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats
```

## 🔐 Безопасность

- **MySQL**: Пароль root/root (измените в production)
- **Backend API**: Доступен только через nginx proxy
- **Frontend**: Статические файлы через nginx

## 🆘 Помощь

- **Подробная документация**: [Docker-README.md](Docker-README.md)
- **Устранение проблем**: Смотрите логи `docker-compose logs`
- **Поддержка**: Создайте issue в репозитории

---

**🎉 Готово! Ваше приложение работает в Docker контейнерах!** 