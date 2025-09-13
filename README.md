# Credit Approval System

A comprehensive Django-based Credit Approval System built as an assignment for Alemeno. Features automated loan approval, customer management, and advanced credit scoring algorithms with full Docker support.

## Table of Contents

- [🚀 Features](#-features)
- [⚡ Quick Start](#-quick-start)
- [🔌 API Endpoints](#-api-endpoints)
- [📊 Credit Scoring](#-credit-scoring)
- [🐳 Docker Setup](#-docker-setup)
- [🧪 Testing](#-testing)
- [📁 Project Structure](#-project-structure)
- [⚙️ Configuration](#️-configuration)
- [💻 Development](#-development)
- [📈 Adding CSV Data](#-adding-csv-data)

## 🚀 Features

- **Automated Credit Scoring**: Advanced algorithm based on payment history, loan activity, and financial metrics
- **Loan Approval System**: Tiered approval logic with interest rate adjustments
- **Customer Management**: Complete CRUD operations with approved limit calculations
- **REST API**: Full REST API with Django REST Framework
- **Docker Support**: Complete containerization with PostgreSQL
- **Data Import**: CSV data import with management commands
- **Comprehensive Testing**: Unit tests, API tests, and database rollback strategies

## ⚡ Quick Start

### Prerequisites

- Python 3.13+
- Docker Desktop (for containerized setup)
- uv package manager

### Local Development

```bash
# Clone and setup
git clone <repository-url>
cd Alemeno

# Install dependencies
uv sync

# Run migrations
python manage.py migrate

# Import sample data
python manage.py import_data

# Start development server
python main.py start
```

### Docker Setup

```bash
# Start entire system with one command
docker-compose up --build

# Access the application
# API: http://localhost:8000/api/
# Database: localhost:5432
```

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/register/` | Register new customer |
| `POST` | `/api/check-eligibility/` | Check loan eligibility |
| `POST` | `/api/create-loan/` | Create new loan |
| `GET` | `/api/view-loan/<id>/` | View loan details |
| `GET` | `/api/view-loans/<customer_id>/` | View customer's loans |
| `GET` | `/api/credit-score/<customer_id>/` | Get customer credit score |
| `GET` | `/api/stats/` | System statistics |

### Example Usage

```bash
# Register customer
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "age": 30,
    "monthly_income": 50000,
    "phone_number": "1234567890"
  }'

# Check loan eligibility
curl -X POST http://localhost:8000/api/check-eligibility/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 12.0,
    "tenure": 24
  }'
```

## 📊 Credit Scoring

The system uses a comprehensive 0-100 credit scoring algorithm:

### Scoring Factors

- **Past Loans Paid on Time**: 30 points maximum
- **Number of Past Loans**: 20 points maximum  
- **Current Year Loan Activity**: 20 points maximum
- **Total Approved Volume**: 20 points maximum
- **Current Debt vs Approved Limit**: 10 points maximum

### Approval Logic

| Credit Score | Interest Rate Requirement | Action |
|--------------|---------------------------|---------|
| > 50 | Any rate | Approve |
| 30-50 | ≥ 12% | Approve |
| 10-30 | ≥ 16% | Approve |
| < 10 | N/A | Reject |

### Additional Checks

- Monthly EMIs must not exceed 50% of monthly salary
- Loan amount must not exceed approved limit
- Age and tenure validation

## 🐳 Docker Setup

### Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Django App    │◄──►│   PostgreSQL    │
│   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘
```

### Commands

```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f

# Database operations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py import_data

# Stop services
docker-compose down
```

### Configuration

- **Database**: `alemeno_credit_system`
- **Username**: `alemeno_user`
- **Password**: Stored in `secrets/db_password.txt`
- **Environment**: Development mode with `DEBUG=1`

## 🧪 Testing

### Test Strategies

**Strategy 1: Database Rollback (Default)**
- Fast execution with automatic rollback
- No permanent database changes
- Best for unit tests and development

**Strategy 2: Separate Test Database**
- Complete isolation from main data
- More realistic testing environment
- Best for integration tests

### Running Tests

```bash
# All tests (unit + API)
python main.py test

# Unit tests only
python main.py unit

# API tests only  
python main.py api

# Advanced options
python bin/run_tests.py --all --separate-db
```

### Test Coverage

- **Model Tests**: Customer and Loan model validation
- **Service Tests**: Credit scoring and loan approval logic
- **API Tests**: Complete endpoint functionality
- **Integration Tests**: Database interactions and workflows

## 📁 Project Structure

```
Alemeno/
├── credit_system/          # Main Django app
│   ├── services/          # Business logic modules
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   └── migrations/        # Database schema changes
├── project/               # Django project settings
├── tests/                 # Test modules
├── bin/                   # Executable scripts
├── logs/                  # Application logs
├── Docs/                  # Documentation and CSV data
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Container definition
└── main.py               # Application launcher
```

### Key Components

- **Services Module**: Split into credit scoring, loan management, and customer management
- **Logging System**: Datetime-stamped logs with comprehensive coverage
- **Management Commands**: CSV data import and system setup
- **Docker Configuration**: Complete containerization with PostgreSQL

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_HOST` | `db` | PostgreSQL hostname |
| `DB_NAME` | `alemeno_credit_system` | Database name |
| `DB_USER` | `alemeno_user` | Database username |
| `DEBUG` | `1` | Django debug mode |

### Database Settings

- **Development**: SQLite fallback if PostgreSQL unavailable
- **Production**: PostgreSQL with Docker secrets
- **Testing**: Automatic rollback or separate test database

## 💻 Development

### Code Quality

```bash
# Linting with Ruff
uv run ruff check .

# Auto-fix issues
uv run ruff check . --fix
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Import data
python manage.py import_data
```

### Main Application Launcher

```bash
# Start server
python main.py start

# Setup database
python main.py setup

# Run tests
python main.py test

# Get help
python main.py help
```

## 📈 Adding CSV Data

### Importing New Customer Data

To add new customer data from CSV files:

```bash
# Import customer data
python manage.py import_data --customer-file path/to/new_customers.csv

# Import loan data
python manage.py import_data --loan-file path/to/new_loans.csv

# Import both files
python manage.py import_data --customer-file customers.csv --loan-file loans.csv
```

### CSV File Formats

**Customer CSV Format:**
```csv
customer_id,first_name,last_name,age,monthly_income,phone_number,approved_limit
1,John,Doe,30,50000,1234567890,1800000
2,Jane,Smith,25,40000,9876543210,1440000
```

**Loan CSV Format:**
```csv
loan_id,customer_id,loan_amount,interest_rate,tenure,monthly_installment,start_date,end_date,emis_paid_on_time
1,1,100000,12.0,24,4707.35,2023-01-01,2024-12-31,12
2,2,80000,15.0,36,2774.39,2023-02-01,2025-01-31,8
```

### Data Validation

The system automatically validates:
- **Customer IDs**: Must be unique integers
- **Phone Numbers**: Must be unique 10-digit numbers
- **Loan IDs**: Must be unique integers
- **Dates**: Must be in YYYY-MM-DD format
- **Financial Data**: Must be positive numbers

### Docker Environment

For Docker deployments, place CSV files in the `Docs/` directory:

```bash
# Copy files to Docs directory
cp new_customers.csv Docs/
cp new_loans.csv Docs/

# Import via Docker
docker-compose exec web python manage.py import_data --customer-file Docs/new_customers.csv --loan-file Docs/new_loans.csv
```

### Bulk Data Operations

```bash
# Clear existing data (use with caution)
python manage.py flush

# Import fresh dataset
python manage.py import_data --customer-file Docs/customer_data.csv --loan-file Docs/loan_data.csv

# Verify import
python manage.py shell -c "from credit_system.models import Customer, Loan; print(f'Customers: {Customer.objects.count()}, Loans: {Loan.objects.count()}')"
```

---

**Built as an assignment for Alemeno** | **Django 5.0+** | **Python 3.13+** | **PostgreSQL** | **Docker**