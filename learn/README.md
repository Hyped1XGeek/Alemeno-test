# PostgreSQL Connection Examples with psycopg2

This directory contains comprehensive examples of connecting to PostgreSQL using psycopg2, specifically configured for your Docker setup with password `Anand123*`.

## 🐘 Database Configuration

Your PostgreSQL database is configured with:
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `credit_system`
- **Username**: `postgres`
- **Password**: `Anand123*`

## 📁 Files Overview

### 1. `connect.py` - Basic Connection
**Purpose**: Simple connection example for beginners
**Features**:
- Basic connection setup
- Simple error handling
- Version and time queries
- Proper connection cleanup

**Usage**:
```bash
python learn/connect.py
```

### 2. `advanced_connect.py` - Advanced Connection
**Purpose**: Comprehensive connection with error handling and retry logic
**Features**:
- Retry logic for failed connections
- Comprehensive error handling
- Database information queries
- Connection testing
- Transaction management

**Usage**:
```bash
python learn/advanced_connect.py
```

### 3. `context_manager.py` - Context Manager
**Purpose**: Safe connection management using context managers
**Features**:
- Automatic resource cleanup
- Transaction handling
- Exception safety
- Both class-based and function-based approaches

**Usage**:
```bash
python learn/context_manager.py
```

### 4. `crud_operations.py` - CRUD Operations
**Purpose**: Complete CRUD (Create, Read, Update, Delete) examples
**Features**:
- User management system
- Full CRUD operations
- Search functionality
- Statistics and reporting
- Batch operations

**Usage**:
```bash
python learn/crud_operations.py
```

### 5. `connection_pool.py` - Connection Pooling
**Purpose**: High-performance connection pooling for concurrent applications
**Features**:
- Thread-safe connection pooling
- Concurrent connection handling
- Performance comparisons
- Pool monitoring
- Transaction support

**Usage**:
```bash
python learn/connection_pool.py
```

## 🚀 Quick Start

### Prerequisites
1. **Docker PostgreSQL running**:
   ```bash
   docker ps  # Check if PostgreSQL container is running
   ```

2. **Install psycopg2**:
   ```bash
   pip install psycopg2-binary
   # or
   uv add psycopg2-binary
   ```

### Running Examples

1. **Start with basic connection**:
   ```bash
   python learn/connect.py
   ```

2. **Try advanced features**:
   ```bash
   python learn/advanced_connect.py
   ```

3. **Learn context managers**:
   ```bash
   python learn/context_manager.py
   ```

4. **Practice CRUD operations**:
   ```bash
   python learn/crud_operations.py
   ```

5. **Explore connection pooling**:
   ```bash
   python learn/connection_pool.py
   ```

## 🔧 Troubleshooting

### Common Issues

1. **Connection Refused**:
   - Check if Docker container is running: `docker ps`
   - Verify port 5432 is accessible: `nmap -p 5432 localhost`
   - Start container: `docker-compose up -d db`

2. **Authentication Failed**:
   - Verify password is `Anand123*`
   - Check username is `postgres`
   - Ensure database `credit_system` exists

3. **Import Errors**:
   - Install psycopg2: `pip install psycopg2-binary`
   - Check Python environment

4. **Permission Errors**:
   - Ensure user has proper database permissions
   - Check if database exists

### Docker Commands
```bash
# Check running containers
docker ps

# View container logs
docker logs <container_name>

# Connect to database directly
docker exec -it <container_name> psql -U postgres -d credit_system

# Restart database container
docker-compose restart db
```

## 📚 Learning Path

### Beginner
1. Start with `connect.py` - Learn basic connection
2. Move to `context_manager.py` - Learn safe connection handling
3. Practice with `crud_operations.py` - Learn database operations

### Intermediate
1. Study `advanced_connect.py` - Learn error handling and retry logic
2. Explore `crud_operations.py` - Master CRUD operations
3. Understand `context_manager.py` - Learn resource management

### Advanced
1. Master `connection_pool.py` - Learn high-performance patterns
2. Combine patterns from all examples
3. Build your own database abstraction layer

## 🎯 Best Practices

### Connection Management
- Always use context managers for automatic cleanup
- Handle exceptions properly
- Use connection pooling for concurrent applications
- Set appropriate timeouts

### Security
- Never hardcode passwords in production
- Use environment variables for credentials
- Implement proper error handling
- Use parameterized queries to prevent SQL injection

### Performance
- Use connection pooling for high-traffic applications
- Implement retry logic for transient failures
- Use batch operations when possible
- Monitor connection usage

## 🔗 Integration with Django

Your Django project is already configured to use this PostgreSQL database. The examples in this directory can be adapted for:

- Custom Django management commands
- Background tasks
- Data migration scripts
- Performance testing
- Custom database operations

## 📖 Additional Resources

- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Django Database Documentation](https://docs.djangoproject.com/en/stable/topics/db/)

## 🤝 Contributing

Feel free to extend these examples with:
- Additional error handling patterns
- More complex query examples
- Performance optimization techniques
- Integration with other Python libraries

---

**Happy coding with PostgreSQL and psycopg2!** 🐘✨
