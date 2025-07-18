# 🏗️ KHTRM System - Оптимизированная структура проекта

## 🎯 **Предлагаемая структура:**

```
khtrm-system/
├── 📁 backend/                     # Python FastAPI Backend
│   ├── 📁 app/                     # Основное приложение
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app точка входа
│   │   ├── config.py               # Конфигурация
│   │   ├── database.py             # База данных
│   │   ├── 📁 models/              # SQLAlchemy модели
│   │   ├── 📁 schemas/             # Pydantic схемы
│   │   ├── 📁 routers/             # API роутеры
│   │   ├── 📁 services/            # Бизнес логика
│   │   └── 📁 utils/               # Утилиты
│   ├── 📁 tests/                   # Тесты (НОВОЕ)
│   │   ├── test_database.py
│   │   ├── test_api.py
│   │   └── test_connection.py
│   ├── 📁 scripts/                 # Скрипты развертывания (НОВОЕ)
│   │   ├── init_database.py
│   │   └── check_connection.py
│   ├── pyproject.toml              # Python зависимости
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   └── README.md
│
├── 📁 frontend/                    # Vue.js Frontend
│   ├── 📁 src/                     # Исходный код Vue.js
│   ├── 📁 public/                  # Статические файлы
│   ├── package.json                # Node.js зависимости
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── Dockerfile
│   ├── nginx.conf
│   └── README.md
│
├── 📁 deployment/                  # Развертывание (НОВОЕ)
│   ├── docker-compose.yml          # Локальная разработка
│   ├── docker-compose.prod.yml     # Продакшн
│   ├── docker-compose.external-db.yml
│   ├── deploy-windows-server.ps1
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   └── scripts/
│       ├── backup.sh
│       └── restore.sh
│
├── 📁 docs/                        # Документация
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
│
├── 📁 .github/                     # CI/CD (опционально)
│   └── workflows/
│       ├── backend-tests.yml
│       └── frontend-build.yml
│
├── .gitignore                      # Git игнорирование
├── README.md                       # Основная документация
└── LICENSE                         # Лицензия
```

## 🔄 **Миграция текущей структуры:**

### **1. Перемещение файлов:**
- `test_*.py` → `backend/tests/`
- `check_databases.py` → `backend/scripts/`
- `docker-compose*.yml` → `deployment/`
- `deploy-windows-server.ps1` → `deployment/`
- Документация → `docs/`

### **2. Создание новых файлов:**
- `backend/.env.example`
- `backend/pyproject.toml` (отдельно от корня)
- `frontend/README.md`
- Новые тестовые файлы

### **3. Обновление путей:**
- Dockerfile пути
- Import paths в Python
- Docker Compose volumes
- Nginx конфигурации

## ✅ **Преимущества новой структуры:**

1. **Четкое разделение** фронтенда и бэкенда
2. **Изолированные зависимости** для каждого сервиса
3. **Централизованное развертывание** в папке deployment/
4. **Структурированные тесты** в backend/tests/
5. **Понятная документация** в docs/
6. **Готовность к CI/CD** с .github/workflows/

## 🚀 **Следующие шаги:**

1. Создать новую структуру директорий
2. Переместить существующие файлы
3. Обновить пути импорта и конфигурации
4. Протестировать новую структуру
5. Обновить документацию

## 🔧 **Совместимость:**

- ✅ Docker контейнеры будут работать
- ✅ Существующие .env файлы совместимы
- ✅ Код приложения не изменится
- ✅ База данных подключения сохранятся

**Хотите выполнить миграцию к новой структуре?** 🤔 