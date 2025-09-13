# 🧪 Credit Approval System - Comprehensive Testing Guide

## 📋 **Testing Strategy Overview**

Your Credit Approval System now supports **two testing strategies** to ensure complete test coverage without database pollution:

### **🔄 Strategy 1: Database Rollback (Default)**
- **How it works**: Uses the same database but rolls back all changes after each test
- **Pros**: Fast execution, simple setup, uses real database structure
- **Cons**: Less realistic, might miss database-specific issues
- **Best for**: Unit tests, development testing, CI/CD pipelines

### **🗄️ Strategy 2: Separate Test Database**
- **How it works**: Creates a completely isolated test database
- **Pros**: Complete isolation, realistic testing, catches DB-specific issues
- **Cons**: Slower execution, requires more setup
- **Best for**: Integration tests, production testing, comprehensive validation

## 🏗️ **Test Structure**

```
tests/
├── __init__.py              # Test package initialization
├── test_models.py           # Unit tests for models
├── test_services.py         # Unit tests for services
├── test_api.py              # API integration tests
└── test_config.py           # Test configuration and strategies
```

## 🧪 **Test Types**

### **1. Unit Tests (`test_models.py`, `test_services.py`)**
- **Purpose**: Test individual components in isolation
- **Database**: Uses rollback by default (no permanent changes)
- **Coverage**: Models, services, business logic
- **Speed**: Fast execution

### **2. Integration Tests (`test_api.py`)**
- **Purpose**: Test complete API endpoints and workflows
- **Database**: Creates minimal test data (marked as test data)
- **Coverage**: Full API functionality, error handling
- **Speed**: Medium execution

## 🚀 **Running Tests**

### **Quick Commands (via main.py)**
```bash
# Run all tests (unit + API)
python main.py test

# Run unit tests only
python main.py unit

# Run API tests only
python main.py api
```

### **Advanced Commands (via test runner)**
```bash
# Unit tests with rollback (default)
python bin/run_tests.py --unit

# Unit tests with separate test database
python bin/run_tests.py --unit --separate-db

# API tests only
python bin/run_tests.py --api

# All tests with separate test database
python bin/run_tests.py --all --separate-db

# Verbose output
python bin/run_tests.py --all --verbosity 2
```

## 📊 **Test Coverage**

### **Model Tests (`test_models.py`)**
- ✅ Customer model creation and validation
- ✅ Loan model creation and validation
- ✅ Model relationships and constraints
- ✅ Business logic methods
- ✅ String representations
- ✅ Field validation and constraints

### **Service Tests (`test_services.py`)**
- ✅ Credit scoring calculations
- ✅ Loan approval logic
- ✅ EMI calculations
- ✅ Interest rate adjustments
- ✅ Customer management operations
- ✅ Loan management operations
- ✅ System statistics

### **API Tests (`test_api.py`)**
- ✅ All API endpoints functionality
- ✅ Request/response validation
- ✅ Error handling
- ✅ Data integrity
- ✅ Authentication (if implemented)

## 🔒 **Database Safety**

### **Automatic Rollback (Default)**
```python
class CustomerModelTest(TestCase):
    def setUp(self):
        # Test data created here
        self.customer = Customer.objects.create(...)
    
    def test_customer_creation(self):
        # Test runs here
        # All changes automatically rolled back after test
        pass
```

**What happens:**
1. Test starts → Database transaction begins
2. Test runs → Changes made to database
3. Test ends → Transaction rolled back
4. **Result**: No permanent changes to database

### **Separate Test Database**
```bash
python bin/run_tests.py --separate-db
```

**What happens:**
1. Creates `test_credit_system` database
2. Runs all migrations on test database
3. Runs tests on isolated database
4. Destroys test database after completion
5. **Result**: Complete isolation from main database

## 🎯 **Test Data Management**

### **Unit Tests**
- **Data**: Created in `setUp()` method
- **Cleanup**: Automatic rollback
- **Impact**: Zero permanent changes
- **IDs**: Use high numbers (99999+) to avoid conflicts

### **API Tests**
- **Data**: Creates minimal test data
- **Cleanup**: Marks as test data (doesn't delete)
- **Impact**: Minimal test records remain
- **IDs**: Uses unique phone numbers and timestamps

## 📈 **Test Execution Examples**

### **Example 1: Unit Tests with Rollback**
```bash
$ python bin/run_tests.py --unit

🧪 Setting up ROLLBACK testing...
   - Uses same database with automatic rollback
   - Fast execution
   - All changes are reverted after each test
   - Best for unit tests and development

🧪 Running Unit Tests...
============================================================
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.234s

OK
Destroying test database for alias 'default'...
✅ All unit tests passed!
```

### **Example 2: Tests with Separate Database**
```bash
$ python bin/run_tests.py --all --separate-db

🗄️  Using SEPARATE TEST DATABASE
   - Complete isolation from main data
   - More realistic testing
   - Slower execution

🧪 Setting up SEPARATE TEST DATABASE...
   - Creates isolated test database
   - Complete isolation from main data
   - More realistic testing
   - Best for integration tests and production

Creating test database for alias 'default'...
Operations to perform:
  Synchronize unmigrated apps: staticfiles, messages
  Apply all migrations: credit_system
Synchronizing apps without migrations:
  Creating tables...
  Running deferred SQL...
Running migrations:
  Applying credit_system.0001_initial... OK
  Applying credit_system.0002_auto_20250912_1804... OK
  Applying credit_system.0003_rename_fields... OK

🧪 Running Unit Tests...
============================================================
...........
----------------------------------------------------------------------
Ran 11 tests in 0.456s

OK

🌐 Running API Tests...
============================================================
⏳ Waiting for server to be ready...
🧪 Credit Approval System - PostgreSQL API Tests
============================================================
...
✅ All tests passed! PostgreSQL integration is working correctly.

Destroying test database for alias 'default'...
✅ All tests passed!
```

## 🛠️ **Customizing Tests**

### **Adding New Unit Tests**
```python
# tests/test_models.py
class NewModelTest(TestCase):
    def setUp(self):
        # Create test data
        self.test_data = {...}
    
    def test_new_functionality(self):
        # Test your new functionality
        # Changes will be automatically rolled back
        pass
```

### **Adding New Service Tests**
```python
# tests/test_services.py
class NewServiceTest(TestCase):
    def setUp(self):
        # Create test data
        self.customer = Customer.objects.create(...)
    
    def test_new_service_method(self):
        # Test your new service method
        result = NewService.new_method(self.customer)
        self.assertEqual(result, expected_value)
```

## 🔍 **Debugging Tests**

### **Verbose Output**
```bash
python bin/run_tests.py --unit --verbosity 2
```

### **Keep Test Database**
```bash
python bin/run_tests.py --separate-db --keepdb
```

### **Run Specific Test**
```bash
python bin/run_tests.py --unit tests.test_models.CustomerModelTest.test_customer_creation
```

## 📋 **Best Practices**

### **1. Test Isolation**
- Each test should be independent
- Use `setUp()` for common test data
- Don't rely on test execution order

### **2. Database Safety**
- Always use high IDs (99999+) for test data
- Use unique phone numbers for customers
- Mark test data clearly

### **3. Test Coverage**
- Test both success and failure cases
- Test edge cases and boundary conditions
- Test validation and error handling

### **4. Performance**
- Use rollback for unit tests (fast)
- Use separate DB for integration tests (thorough)
- Keep tests focused and specific

## 🎉 **Summary**

Your Credit Approval System now has:

✅ **Comprehensive unit tests** for models and services
✅ **API integration tests** for complete workflows
✅ **Database rollback** for fast, safe unit testing
✅ **Separate test database** for complete isolation
✅ **Automatic cleanup** - no permanent database changes
✅ **Multiple test strategies** for different needs
✅ **Easy test execution** via main.py or test runner
✅ **Detailed logging** and error reporting

**Default behavior**: All tests use database rollback (no permanent changes)
**Production testing**: Use `--separate-db` for complete isolation
**Development**: Use default rollback for fast iteration

Your tests are now **completely safe** and won't pollute your database! 🎉
