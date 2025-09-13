# Credit Approval System

A comprehensive Django-based Credit Approval System that provides loan approval functionality, customer management, and credit scoring algorithms.

## Features

- **Customer Management**: Complete CRUD operations for customer data
- **Loan Management**: Track and manage loan applications and approvals
- **Credit Scoring**: Advanced credit scoring algorithm based on multiple factors
- **Credit Approval**: Automated loan approval/rejection with detailed reasoning
- **REST API**: Full REST API for all operations
- **Data Import**: Import customer and loan data from CSV files
- **Admin Interface**: Django admin interface for data management

## Project Structure

```
Alemeno/
├── project/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── credit_system/          # Main Django app
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py          # Customer and Loan models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # App URL configuration
│   ├── admin.py           # Admin configuration
│   ├── services.py        # Business logic services
│   └── management/
│       └── commands/
│           └── import_data.py  # Data import command
├── Docs/                   # Documentation and data files
│   ├── customer_data.csv
│   └── loan_data.csv
├── bin/                    # Executable scripts
├── logs/                   # Log files
├── templates/              # Django templates
├── staticfiles/            # Static files
├── manage.py              # Django management script
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Installation and Setup

### Prerequisites

- Python 3.13+
- uv package manager

### 1. Install Dependencies

```bash
# Install uv if not already installed
pip install uv

# Install project dependencies
uv sync
```

### 2. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 3. Import Sample Data

```bash
# Import customer and loan data from CSV files
python manage.py import_data
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Customer Endpoints

- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create a new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer
- `GET /api/customers/search/?q={query}` - Search customers
- `GET /api/customers/{id}/loans/` - Get customer's loans
- `GET /api/customers/{id}/summary/` - Get customer loan summary

### Loan Endpoints

- `GET /api/loans/` - List all loans
- `POST /api/loans/` - Create a new loan
- `GET /api/loans/{id}/` - Get loan details
- `PUT /api/loans/{id}/` - Update loan
- `DELETE /api/loans/{id}/` - Delete loan
- `GET /api/loans/active/` - Get active loans

### Credit Approval Endpoints

- `POST /api/credit-approval/` - Submit credit approval request

### System Endpoints

- `GET /api/stats/` - Get system statistics

## Credit Approval API Usage

### Submit Credit Approval Request

```bash
curl -X POST http://localhost:8000/api/credit-approval/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 100000,
    "tenure": 24,
    "interest_rate": 12.5
  }'
```

### Response Format

```json
{
  "approved": true,
  "message": "Loan approved",
  "loan_id": 12345,
  "credit_score": 750,
  "monthly_payment": 4500.00,
  "total_amount": 108000.00,
  "reasons": ["Loan approved based on all criteria"]
}
```

## Credit Scoring Algorithm

The system uses a comprehensive credit scoring algorithm that considers:

1. **Age Factor**: Older customers get higher scores
2. **Salary Factor**: Higher salaries result in better scores
3. **Credit Utilization**: Lower utilization ratios improve scores
4. **Payment History**: On-time payment history increases scores
5. **Loan Amount vs. Salary**: Monthly payment should not exceed 40% of salary
6. **Credit Limit**: Loan amount should not exceed approved limit

### Credit Score Ranges

- **300-579**: Poor credit
- **580-669**: Fair credit
- **670-739**: Good credit
- **740-799**: Very good credit
- **800-850**: Excellent credit

## Data Models

### Customer Model

```python
{
  "customer_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "age": 35,
  "phone_number": "1234567890",
  "monthly_salary": 50000.00,
  "approved_limit": 500000.00,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Loan Model

```python
{
  "loan_id": 12345,
  "customer": 1,
  "loan_amount": 100000.00,
  "tenure": 24,
  "interest_rate": 12.50,
  "monthly_payment": 4500.00,
  "emis_paid_on_time": 12,
  "date_of_approval": "2024-01-01",
  "end_date": "2026-01-01",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## Development

### Code Quality

The project uses Ruff for linting and follows PEP 8 standards:

```bash
# Run linting
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check . --fix
```

### Running Tests

```bash
# Run tests (when implemented)
python manage.py test
```

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py import_data
```

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to:

- Manage customers and loans
- View system statistics
- Monitor credit approvals
- Import/export data

## Configuration

### Environment Variables

Create a `.env` file for production settings:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Logging

Logs are written to `logs/django.log` and console output. Configure logging levels in `project/settings.py`.

## Production Deployment

### Using Docker

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Using Render/Heroku

1. Set environment variables
2. Configure database
3. Run migrations
4. Import data
5. Deploy

## API Documentation

### Authentication

Currently, the API allows anonymous access. For production, implement authentication:

```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Rate Limiting

Implement rate limiting for production:

```python
# Add to settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## Troubleshooting

### Common Issues

1. **Database errors**: Run migrations and check database permissions
2. **Import errors**: Ensure CSV files are in the correct format
3. **Permission errors**: Check file permissions for logs and static files
4. **Port conflicts**: Change the port in runserver command

### Debug Mode

Enable debug mode in development:

```python
# In settings.py
DEBUG = True
```

## Contributing

1. Follow PEP 8 style guidelines
2. Use Ruff for linting
3. Write comprehensive tests
4. Update documentation
5. Submit pull requests

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please create an issue in the project repository.
