#!/usr/bin/env python3
"""
PostgreSQL connection pool example using psycopg2.pool.
This demonstrates how to use connection pooling for better performance.
"""

import psycopg2
import psycopg2.pool
import psycopg2.extras
from psycopg2 import Error
import threading
import time
import random
from contextlib import contextmanager


class DatabasePool:
    """PostgreSQL connection pool manager."""
    
    def __init__(self, min_connections=2, max_connections=10, 
                 host='localhost', port='5432', database='credit_system', 
                 user='postgres', password='Anand123*'):
        
        self.connection_params = {
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password
        }
        
        self.pool = None
        self.min_connections = min_connections
        self.max_connections = max_connections
        
        self._create_pool()
    
    def _create_pool(self):
        """Create the connection pool."""
        try:
            print(f"🏊 Creating connection pool (min: {self.min_connections}, max: {self.max_connections})...")
            
            self.pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=self.min_connections,
                maxconn=self.max_connections,
                **self.connection_params
            )
            
            print("✅ Connection pool created successfully!")
            
        except Error as e:
            print(f"❌ Error creating connection pool: {e}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Get a connection from the pool."""
        connection = None
        try:
            connection = self.pool.getconn()
            yield connection
        except Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                self.pool.putconn(connection)
    
    @contextmanager
    def get_cursor(self):
        """Get a cursor from the pool."""
        connection = None
        cursor = None
        try:
            connection = self.pool.getconn()
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor
            )
            yield cursor
        except Error as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if connection:
                self.pool.putconn(connection)
    
    def close_all(self):
        """Close all connections in the pool."""
        if self.pool:
            self.pool.closeall()
            print("🔌 All connections in pool closed")
    
    def get_pool_status(self):
        """Get the current status of the connection pool."""
        if self.pool:
            return {
                'min_connections': self.min_connections,
                'max_connections': self.max_connections,
                'closed': self.pool.closed
            }
        return None


def demo_basic_pool_usage():
    """Demonstrate basic connection pool usage."""
    
    print("🏊 Basic Connection Pool Demo")
    print("-" * 40)
    
    # Create connection pool
    db_pool = DatabasePool(min_connections=2, max_connections=5)
    
    try:
        # Test basic connection
        with db_pool.get_cursor() as cursor:
            cursor.execute("SELECT version();")
            result = cursor.fetchone()
            print(f"✅ Connected via pool: {result['version'][:50]}...")
        
        # Test multiple connections
        print("\n🔄 Testing multiple connections...")
        for i in range(3):
            with db_pool.get_cursor() as cursor:
                cursor.execute("SELECT current_database(), current_user, NOW();")
                result = cursor.fetchone()
                print(f"  Connection {i+1}: DB={result['current_database']}, User={result['current_user']}")
        
        # Get pool status
        status = db_pool.get_pool_status()
        print(f"\n📊 Pool Status: {status}")
        
    finally:
        db_pool.close_all()


def demo_concurrent_connections():
    """Demonstrate concurrent connections using the pool."""
    
    print("\n🚀 Concurrent Connections Demo")
    print("-" * 40)
    
    db_pool = DatabasePool(min_connections=3, max_connections=8)
    
    def worker_thread(thread_id, num_operations=5):
        """Worker thread function."""
        print(f"🧵 Thread {thread_id} starting...")
        
        for i in range(num_operations):
            try:
                with db_pool.get_cursor() as cursor:
                    # Simulate some work
                    cursor.execute("SELECT pg_sleep(%s), NOW() as current_time;", (random.uniform(0.1, 0.5),))
                    result = cursor.fetchone()
                    print(f"  Thread {thread_id}, Op {i+1}: {result['current_time']}")
                    
            except Error as e:
                print(f"❌ Thread {thread_id} error: {e}")
        
        print(f"✅ Thread {thread_id} completed")
    
    try:
        # Create and start multiple threads
        threads = []
        num_threads = 5
        
        print(f"Starting {num_threads} concurrent threads...")
        
        for i in range(num_threads):
            thread = threading.Thread(target=worker_thread, args=(i+1, 3))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        print("✅ All threads completed successfully!")
        
    finally:
        db_pool.close_all()


def demo_pool_performance():
    """Demonstrate pool performance vs single connections."""
    
    print("\n⚡ Performance Comparison Demo")
    print("-" * 40)
    
    # Test with connection pool
    print("🏊 Testing with connection pool...")
    db_pool = DatabasePool(min_connections=3, max_connections=6)
    
    start_time = time.time()
    num_operations = 20
    
    try:
        for i in range(num_operations):
            with db_pool.get_cursor() as cursor:
                cursor.execute("SELECT 1 + %s as result;", (i,))
                result = cursor.fetchone()
        
        pool_time = time.time() - start_time
        print(f"✅ Pool operations completed in {pool_time:.3f} seconds")
        
    finally:
        db_pool.close_all()
    
    # Test with single connections
    print("\n🔌 Testing with single connections...")
    start_time = time.time()
    
    for i in range(num_operations):
        try:
            connection = psycopg2.connect(
                host='localhost',
                port='5432',
                database='credit_system',
                user='postgres',
                password='Anand123*'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT 1 + %s as result;", (i,))
            result = cursor.fetchone()
            cursor.close()
            connection.close()
        except Error as e:
            print(f"❌ Single connection error: {e}")
    
    single_time = time.time() - start_time
    print(f"✅ Single connection operations completed in {single_time:.3f} seconds")
    
    # Performance comparison
    print(f"\n📊 Performance Comparison:")
    print(f"  Pool time: {pool_time:.3f}s")
    print(f"  Single time: {single_time:.3f}s")
    print(f"  Speedup: {single_time/pool_time:.2f}x faster with pool")


def demo_pool_with_transactions():
    """Demonstrate using connection pool with transactions."""
    
    print("\n💳 Pool with Transactions Demo")
    print("-" * 40)
    
    db_pool = DatabasePool(min_connections=2, max_connections=4)
    
    try:
        # Create a test table
        with db_pool.get_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pool_test (
                    id SERIAL PRIMARY KEY,
                    thread_id INTEGER,
                    operation_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.connection.commit()
            print("✅ Test table created")
        
        def transaction_worker(thread_id, num_operations=3):
            """Worker that performs transactions."""
            print(f"🧵 Thread {thread_id} starting transactions...")
            
            for i in range(num_operations):
                try:
                    with db_pool.get_connection() as connection:
                        cursor = connection.cursor()
                        
                        # Start transaction
                        cursor.execute("BEGIN;")
                        
                        # Insert data
                        cursor.execute("""
                            INSERT INTO pool_test (thread_id, operation_id)
                            VALUES (%s, %s);
                        """, (thread_id, i+1))
                        
                        # Simulate some work
                        cursor.execute("SELECT pg_sleep(%s);", (random.uniform(0.1, 0.3),))
                        
                        # Commit transaction
                        cursor.execute("COMMIT;")
                        print(f"  Thread {thread_id}, Op {i+1}: Transaction committed")
                        
                except Error as e:
                    print(f"❌ Thread {thread_id} transaction error: {e}")
                    if connection:
                        connection.rollback()
        
        # Run concurrent transactions
        threads = []
        for i in range(3):
            thread = threading.Thread(target=transaction_worker, args=(i+1, 2))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Check results
        with db_pool.get_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as total FROM pool_test;")
            result = cursor.fetchone()
            print(f"✅ Total records created: {result['total']}")
            
            cursor.execute("SELECT thread_id, COUNT(*) as count FROM pool_test GROUP BY thread_id ORDER BY thread_id;")
            results = cursor.fetchall()
            print("📊 Records per thread:")
            for row in results:
                print(f"  Thread {row['thread_id']}: {row['count']} records")
        
    finally:
        db_pool.close_all()


def demo_pool_monitoring():
    """Demonstrate pool monitoring and statistics."""
    
    print("\n📊 Pool Monitoring Demo")
    print("-" * 40)
    
    db_pool = DatabasePool(min_connections=2, max_connections=5)
    
    try:
        # Get initial pool status
        status = db_pool.get_pool_status()
        print(f"Initial pool status: {status}")
        
        # Simulate some load
        print("\n🔄 Simulating database load...")
        
        def load_worker(worker_id, duration=3):
            """Worker that creates load on the pool."""
            start_time = time.time()
            operations = 0
            
            while time.time() - start_time < duration:
                try:
                    with db_pool.get_cursor() as cursor:
                        cursor.execute("SELECT pg_sleep(%s), NOW();", (0.1,))
                        operations += 1
                except Error as e:
                    print(f"❌ Worker {worker_id} error: {e}")
            
            print(f"  Worker {worker_id}: {operations} operations in {duration}s")
        
        # Start multiple workers
        workers = []
        for i in range(4):
            worker = threading.Thread(target=load_worker, args=(i+1, 2))
            workers.append(worker)
            worker.start()
        
        # Wait for workers
        for worker in workers:
            worker.join()
        
        # Final pool status
        final_status = db_pool.get_pool_status()
        print(f"\nFinal pool status: {final_status}")
        
    finally:
        db_pool.close_all()


def main():
    """Main function to run all pool demos."""
    
    print("🐘 PostgreSQL Connection Pool Examples")
    print("=" * 60)
    
    try:
        demo_basic_pool_usage()
        demo_concurrent_connections()
        demo_pool_performance()
        demo_pool_with_transactions()
        demo_pool_monitoring()
        
        print("\n🏁 All connection pool demos completed!")
        
    except Error as e:
        print(f"❌ Database error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
