# 🚚 KHTRM System - Kharkiv Transport Resource Management

> **✨ Modern transport fleet management system with advanced admin interface and role-based access control**

A comprehensive Kharkiv Transport Resource Management (KHTRM) system designed for transport fleet operations in Kharkiv city. Built with FastAPI backend, Vue 3 frontend, and MySQL database, featuring role-based user interfaces, advanced admin tools, and modern architecture.

## 🎯 Key Features

### 🔐 Role-Based Access Control

- **Super Admin** - Full system access with advanced admin dashboard
- **Dispatcher** (нарядчик) - Creates transport assignments and schedules
- **Timekeeper** (табельщик) - Records incidents and work hours
- **Parking Manager** - Manages vehicle parking and return operations
- **Fuel Manager** - Handles fuel operations and consumption tracking
- **Extensible Role System** - Easy to add new roles (mechanic, driver, inspector, analyst)

### 🎛️ Advanced Admin Interface

- **Admin Dashboard** - Comprehensive control panel with multiple management sections
- **Table Constructor** - ✅ Create custom tables with selected columns from any database table
- **Custom Field Builder** - ✅ Create calculated fields, joins, and custom data transformations
- **Database Monitor** - Real-time database structure monitoring and exploration
- **Field Settings** - Configure field visibility and order for different user roles
- **User Management** - Manage users, roles, and permissions (planned)
- **System Settings** - Configure system parameters and preferences (planned)

### 🏗️ Modern Architecture

- **FastAPI Backend** - High-performance Python web framework with full API documentation
- **Vue 3 + TypeScript Frontend** - Modern composables-based architecture with complete type safety
- **MySQL Database** - Robust data storage with proper relationships and real transport data
- **Role-Based UI** - Different interfaces for each user role with adaptive layouts
- **Ukrainian Interface** - User-friendly Ukrainian language interface throughout the system
- **Clean Code** - Production-ready code with Ruff, ESLint, and TypeScript linting

### 🔧 Developer Experience

- **uv Package Manager** - Fast Python dependency management
- **Vite Build System** - Lightning-fast frontend development with TypeScript
- **Full Type Safety** - Complete TypeScript integration with Pydantic schemas
- **Code Quality** - Automated linting, formatting, and type checking
- **Clean Codebase** - English comments, Ukrainian UI, production-ready
- **Extensible Design** - Easy to add new features and roles

## 🏗️ Architecture Overview

```
khtrm-system/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── user.py        # User and Role models
│   │   │   ├── assignment.py  # ✅ Assignment models
│   │   │   ├── employee.py    # Employee models
│   │   │   ├── vehicle.py     # Vehicle models
│   │   │   ├── route.py       # Route models
│   │   │   └── base.py        # Base model with timestamps
│   │   ├── schemas/           # Pydantic Schemas
│   │   │   └── user.py        # User validation schemas
│   │   ├── services/          # Business Logic
│   │   │   └── assignment_service.py  # ✅ Assignment service
│   │   ├── routers/           # API Routes
│   │   │   └── dispatcher.py  # ✅ Dispatcher & Admin routes
│   │   ├── utils/             # Utilities
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database setup
│   │   └── main.py            # FastAPI App
├── frontend/                   # Vue 3 + TypeScript Frontend
│   ├── src/
│   │   ├── components/        # Vue Components (TypeScript)
│   │   │   ├── Dashboard.vue          # Role-based main dashboard
│   │   │   ├── AdminDashboard.vue     # ✅ Admin control panel
│   │   │   ├── TableConstructor.vue   # ✅ Custom table builder
│   │   │   ├── CustomFieldBuilder.vue # ✅ Advanced field builder
│   │   │   ├── DatabaseMonitor.vue    # ✅ Database structure explorer
│   │   │   ├── AdminFieldSettings.vue # ✅ Field configuration
│   │   │   ├── AssignmentTable.vue    # ✅ Assignment management
│   │   │   ├── LoginForm.vue          # Authentication
│   │   │   └── ...other components
│   │   ├── composables/       # Vue 3 Composables (TypeScript)
│   │   │   ├── useAuth.ts     # Authentication composable
│   │   │   └── useNotifications.ts  # ✅ Notifications
│   │   ├── types/             # TypeScript Type Definitions
│   │   │   ├── index.ts       # General types
│   │   │   └── dispatcher.ts  # ✅ Assignment types
│   │   ├── services/          # API Services
│   │   └── main.ts            # Vue App Entry (TypeScript)
│   └── index.html             # HTML Template
├── scripts/                    # Development & Analysis Scripts
├── docs/                       # Documentation
├── deployment/                 # Docker & deployment configs
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

2. **Start the frontend development server (TypeScript)**
   ```bash
   npm run dev
   ```

3. **Access the application**
   - Frontend: http://localhost:3000 (Vue 3 + TypeScript)
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔐 Test Users & Current Status

### Available Test Users

The system currently includes 5 predefined test users:

| Username | Password | Role | Ukrainian Name | Interface |
|----------|----------|------|----------------|-----------|
| `admin` | `admin` | super_admin | Супер Адміністратор | **✅ Admin Dashboard** |
| `nar` | `nar` | dispatcher | Нарядчик | **✅ Assignment Tables** |
| `taba` | `taba` | timekeeper_a | Табельник A | Welcome Screen |
| `tabb` | `tabb` | timekeeper_b | Табельник B | Welcome Screen |
| `dys` | `dys` | dispatcher_main | Диспетчер | Welcome Screen |
| `buc` | `buc` | fuel_accountant | Бухгалтер з палива | Welcome Screen |

### Current Functionality

#### ✅ Fully Implemented Features

**🎛️ Admin Dashboard System**
- **Database Monitoring** - Real-time database structure exploration with table/column information
- **Table Constructor** - Create custom tables with selected columns from any database table
- **Field Settings** - Configure field visibility and ordering for different user roles
- **Admin Navigation** - Tabbed interface with overview, monitoring, and management sections
- **Responsive Design** - Mobile-friendly admin interface with adaptive layouts

**🚚 Dispatcher System**
- **Real-time Assignment Tables** - Live data from MySQL with 182,494+ records
- **Customizable Field Display** - Admin-configurable field selection and ordering
- **Data Integration** - Real-time data from MySQL database (Ukrainian transport assignments)
- **Export Capabilities** - Field settings saved in localStorage
- **Role-based Access** - Different interfaces for different user roles

**🔧 System Infrastructure**
- **TypeScript Migration** - ✅ Complete migration with type safety
- **Authentication System** - Working login/logout with role-based routing
- **Real Database** - ✅ Connected to MySQL with production transport data
- **Clean Codebase** - Production-ready, linting-compliant code
- **Modern UI** - Font Awesome icons, responsive design, Ukrainian localization

#### 🔄 In Development

**User Management System**
- User creation and role assignment
- Permission management interface
- User activity tracking

**Advanced Analytics**
- Transport route optimization
- Fuel consumption analysis
- Performance metrics and reporting

**Additional Role Interfaces**
- Timekeeper incident recording
- Parking manager vehicle tracking
- Fuel manager operations

### Database Integration

- **Production MySQL** - Connected to remote MySQL database
- **Assignment Data** - 182,494+ real transport assignment records
- **Date Range** - Data from 2021-09-01 to 2025-07-11
- **Route Coverage** - Multiple transport routes (17, 20, 21, 22, 29, 31, etc.)
- **Driver Information** - Real driver names, brigade assignments, and schedules
- **Vehicle Data** - Actual vehicle numbers and state registration numbers

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

**TypeScript Frontend:**
```bash
# Lint and format
npm run lint
npm run format

# Type checking
npm run type-check

# Comprehensive check
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
- **Database Monitoring** - Real-time structure exploration

## ✅ Implemented Features

### 🎛️ Admin Dashboard (Fully Implemented)

**Database Monitoring**
- Real-time database structure exploration
- Table and column information with data types
- Row count and column count display
- Search functionality for tables and fields
- Sample data preview

**Table Constructor**
- Create custom tables with selected columns from any database table
- Support for multiple database sources with automatic discovery
- Drag-and-drop style column ordering with up/down arrows
- Real-time preview functionality with actual data
- **Custom Field Builder** - ✅ Create calculated fields, joins, and custom data transformations
- Save and load table configurations to localStorage
- Export table definitions and share configurations

**Custom Field Builder Features:**
- **Calculated Fields** - Time differences, date differences, arithmetic operations
- **Field Concatenation** - Combine multiple fields with custom separators
- **Conditional Logic** - IF-THEN-ELSE logic based on field values
- **JOIN Operations** - Join with other tables to display related data
- **Aggregate Functions** - COUNT, SUM, AVG, MIN, MAX with grouping
- **Lookup Fields** - Search values in reference tables
- **Real-time SQL Preview** - See generated SQL before applying
- **Field Validation** - Ensure all required parameters are provided

**Field Settings Management**
- Configure field visibility for different user roles
- Reorder fields with intuitive interface
- Role-specific field configurations
- Reset to default settings
- Persistent settings storage

### 🚚 Dispatcher Module (Fully Implemented)

**Assignment Management**
- Real-time assignment tables with 182,494+ records
- Date-based filtering and navigation
- Assignment statistics and analytics
- Field customization based on admin settings
- Export capabilities
- Mobile-responsive design

**Data Integration**
- Live MySQL database connection
- Real Kharkiv city transport data
- Multiple route support
- Driver and vehicle information
- Historical data access

## 🔮 Future Features

### 🎯 Planned Enhancements

**User Management System**
- Complete user creation and editing interface
- Role assignment and permission management
- User activity tracking and audit logs
- Bulk user operations

**Advanced Analytics Dashboard**
- Transport route optimization algorithms
- Fuel consumption analysis and reporting
- Performance metrics and KPIs
- Predictive analytics for maintenance

**Mobile Application**
- iOS/Android applications
- Real-time GPS tracking
- Driver mobile interface
- Push notifications

**Extended Role Interfaces**
- Timekeeper incident recording system
- Parking manager vehicle tracking
- Fuel manager operations dashboard
- Mechanic maintenance scheduling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Follow code quality standards
5. Submit a pull request

### Code Standards

- **Python:** Follow PEP 8 with Ruff linting
- **TypeScript:** Strict type checking with ESLint + Vue integration
- **Vue:** Follow Vue 3 Composition API patterns with TypeScript
- **Database:** Use Alembic for migrations
- **Language Policy:** English code/comments, Ukrainian user interface
- **Code Quality:** Clean, production-ready, linting-compliant codebase

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation in `/docs`
- Review the API documentation at `/docs` endpoint

---

**🎉 KHTRM System with fully implemented Admin Dashboard, Database Monitoring, Table Constructor, Custom Field Builder, and Dispatcher modules is ready for production deployment in Kharkiv city transport system!** 