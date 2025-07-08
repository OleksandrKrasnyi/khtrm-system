# 🚚 KHTRM System - Kharkiv Transport Resource Management

> **✨ Modern transport fleet management system with role-based access control**

A comprehensive Kharkiv Transport Resource Management (KHTRM) system designed for transport fleet operations in Kharkiv city. Built with FastAPI backend, Vue 3 frontend, and MySQL database, featuring role-based user interfaces and modern architecture.

## 🎯 Key Features

### 🔐 Role-Based Access Control

- **Super Admin** - Full system access and management
- **Dispatcher** (нарядчик) - Creates transport assignments and schedules
- **Timekeeper** (табельщик) - Records incidents and work hours
- **Parking Manager** - Manages vehicle parking and return operations
- **Fuel Manager** - Handles fuel operations and consumption tracking
- **Extensible Role System** - Easy to add new roles (mechanic, driver, inspector, analyst)

### 🏗️ Modern Architecture

- **FastAPI Backend** - High-performance Python web framework
- **Vue 3 Frontend** - Modern composables-based architecture
- **MySQL Database** - Robust data storage with proper relationships
- **Role-Based UI** - Different interfaces for each user role
- **Ukrainian Interface** - User-friendly Ukrainian language interface
- **Clean Code** - Follows best practices with Ruff, ESLint, and Prettier

### 🔧 Developer Experience

- **uv Package Manager** - Fast Python dependency management
- **Vite Build System** - Lightning-fast frontend development
- **Type Safety** - Pydantic schemas and TypeScript support
- **Code Quality** - Automated linting and formatting
- **Extensible Design** - Easy to add new features and roles

## 🏗️ Architecture Overview

```
khtrm-system/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── user.py        # User and Role models
│   │   │   └── base.py        # Base model with timestamps
│   │   ├── schemas/           # Pydantic Schemas
│   │   │   └── user.py        # User validation schemas
│   │   ├── services/          # Business Logic
│   │   ├── routers/           # API Routes
│   │   ├── utils/             # Utilities
│   │   ├── config.py          # Configuration
│   │   └── main.py            # FastAPI App
│   └── alembic/               # Database Migrations
├── frontend/                   # Vue 3 Frontend
│   ├── src/
│   │   ├── components/        # Vue Components
│   │   ├── composables/       # Vue 3 Composables
│   │   ├── services/          # API Services
│   │   └── main.js            # Vue App Entry
│   └── index.html             # HTML Template
├── scripts/                    # Development Scripts
├── docs/                       # Documentation
├── pyproject.toml             # Python Dependencies
└── package.json               # JavaScript Dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MySQL 8.0+ (or SQLite for development)
- uv (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd khtrm-system
   ```

2. **Install Python dependencies**
   ```bash
   uv sync
   ```

3. **Install JavaScript dependencies**
   ```bash
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

### Development

1. **Start the backend server**
   ```bash
   uv run uvicorn backend.app.main:app --reload
   ```

2. **Start the frontend development server**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔐 Test Users & Current Status

### Available Test Users

The system currently includes 5 predefined test users:

| Username | Password | Role | Ukrainian Name |
|----------|----------|------|----------------|
| `nar` | `nar` | dispatcher | Нарядчик |
| `taba` | `taba` | timekeeper_a | Табельник A |
| `tabb` | `tabb` | timekeeper_b | Табельник B |
| `dys` | `dys` | dispatcher_main | Диспетчер |
| `buc` | `buc` | fuel_accountant | Бухгалтер з палива |

### Current Functionality

- **Simple Login** - Use any of the 5 test accounts
- **Role-Based Greeting** - Shows personalized "Привіт, [Role Name]!" message
- **User Information** - Displays username and email
- **Simple Logout** - Clean session termination
- **Responsive Design** - Works on desktop and mobile

### Future Role Definitions

| Role | Ukrainian | Permissions (Planned) |
|------|-----------|----------------------|
| **Super Admin** | Супер Адміністратор | Full system access |
| **Dispatcher** | Нарядчик | Create assignments, manage schedules |
| **Timekeeper** | Табельщик | Record incidents, track work hours |
| **Parking Manager** | Менеджер стоянки | Manage vehicle parking/return |
| **Fuel Manager** | Менеджер палива | Handle fuel operations |
| **Mechanic** | Механік | Maintenance operations |
| **Driver** | Водій | Driver interface |
| **Inspector** | Інспектор | Quality control |
| **Analyst** | Аналітик | Reports and analytics |

### Permission System

Each role has specific permissions:

- `can_manage_users` - User and role management
- `can_manage_vehicles` - Vehicle fleet management
- `can_create_assignments` - Transport assignments
- `can_record_incidents` - Incident recording
- `can_manage_parking` - Parking operations
- `can_manage_fuel` - Fuel operations
- `can_view_reports` - Analytics access
- `can_manage_system` - System settings

## 🗄️ Database Schema

### Core Tables

- **users** - User accounts with authentication
- **user_roles** - Role definitions with permissions
- **vehicles** - Transport fleet (planned)
- **assignments** - Transport assignments (planned)
- **incidents** - Incident records (planned)
- **fuel_records** - Fuel consumption (planned)

### User Model Features

- **Authentication** - Secure password hashing
- **Role Assignment** - Flexible role-based permissions
- **Profile Management** - Personal information
- **Activity Tracking** - Login history and statistics
- **Ukrainian Support** - Full Ukrainian language support

## 🔧 Development Tools

### Code Quality

**Python Backend:**
```bash
# Check code quality
uv run ruff check
uv run ruff format

# Run tests
uv run pytest
```

**JavaScript Frontend:**
```bash
# Lint and format
npm run lint
npm run format
npm run check:all
```

### Database Operations

```bash
# Create migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

## 📦 Production Deployment

### Environment Setup

1. **Configure MySQL database**
   ```env
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=brm_user
   MYSQL_PASSWORD=secure_password
   MYSQL_DATABASE=brm_system
   ```

2. **Set security settings**
   ```env
   SECRET_KEY=your-super-secret-key-here
   DEBUG=false
   ```

3. **Build frontend**
   ```bash
   npm run build
   ```

4. **Run production server**
   ```bash
   uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```

### Windows Server Deployment

For Windows Server 2022 deployment:

1. Install Python 3.11+
2. Install Node.js 18+
3. Install MySQL 8.0+
4. Configure IIS or use uvicorn directly
5. Set up SSL certificates
6. Configure firewall rules

## 🛠️ Configuration

### Backend Configuration

Edit `backend/app/config.py` for:

- Database connections
- JWT authentication settings
- CORS configuration
- File upload settings
- Email configuration (future)

### Frontend Configuration

Edit `vite.config.js` for:

- API endpoints
- Build optimization
- Development server settings

## 🔒 Security Features

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - Bcrypt password protection
- **Role-Based Access** - Granular permissions
- **Input Validation** - Pydantic schema validation
- **CORS Configuration** - Proper cross-origin settings
- **SQL Injection Protection** - SQLAlchemy ORM
- **Ukrainian Error Messages** - User-friendly validation

## 📊 Monitoring & Logging

- **Request Logging** - All API requests logged
- **Error Tracking** - Comprehensive error handling
- **Performance Monitoring** - Built-in metrics
- **User Activity** - Login and action tracking

## 🔮 Future Features

- **Vehicle Management** - Fleet tracking and maintenance
- **Route Planning** - Optimal route calculations
- **Fuel Optimization** - Consumption analytics
- **Driver Performance** - Performance metrics
- **Mobile App** - iOS/Android applications
- **Real-time Tracking** - GPS vehicle tracking
- **Maintenance Scheduling** - Automated maintenance alerts
- **Reporting Dashboard** - Advanced analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Follow code quality standards
5. Submit a pull request

### Code Standards

- **Python:** Follow PEP 8 with Ruff
- **JavaScript:** Use ESLint + Prettier
- **Vue:** Follow Vue 3 Composition API patterns
- **Database:** Use Alembic for migrations
- **Documentation:** English docs, Ukrainian UI

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation in `/docs`
- Review the API documentation at `/docs` endpoint

---

**🎉 Ready for production deployment in Kharkiv city transport system!** 