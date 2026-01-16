#!/usr/bin/env python3
"""
Diagnostic script to test employee ID verification functionality
This script tests the database connection and simulates the /check-emp-id endpoint
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import *
from pymysql import connections

def test_database_connection():
    """Test basic database connectivity"""
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    try:
        print(f"Attempting to connect to database...")
        print(f"Host: {customhost}")
        print(f"User: {customuser}")
        print(f"Database: {customdb}")
        
        # Create connection
        db_conn = connections.Connection(
            host=customhost,
            port=3306,
            user=customuser,
            password=custompass,
            db=customdb
        )
        
        print("✓ Database connection successful!")
        
        # Test basic query
        cursor = db_conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✓ Basic query successful: {result}")
        
        # Check if employee table exists
        cursor.execute("SHOW TABLES LIKE 'employee'")
        table_exists = cursor.fetchone()
        if table_exists:
            print(f"✓ Employee table exists: {table_exists}")
        else:
            print("✗ Employee table NOT FOUND!")
        
        # Check table structure
        cursor.execute("DESCRIBE employee")
        columns = cursor.fetchall()
        print("\nTable Structure:")
        for col in columns:
            print(f"  {col[0]}: {col[1]}")
        
        cursor.close()
        db_conn.close()
        print("✓ Database connection closed properly")
        
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_employee_id_check(emp_id):
    """Test the employee ID check functionality"""
    print("\n" + "=" * 60)
    print(f"EMPLOYEE ID CHECK TEST (ID: {emp_id})")
    print("=" * 60)
    
    try:
        db_conn = connections.Connection(
            host=customhost,
            port=3306,
            user=customuser,
            password=custompass,
            db=customdb
        )
        
        cursor = db_conn.cursor()
        
        # Test 1: Check if ID exists (should return empty if new)
        print(f"\n1. Checking if employee ID {emp_id} exists...")
        cursor.execute("SELECT emp_id FROM employee WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        
        if result:
            print(f"   ✗ Employee ID {emp_id} ALREADY EXISTS in database")
        else:
            print(f"   ✓ Employee ID {emp_id} is available (not found in database)")
        
        # Test 2: Count total employees
        print("\n2. Counting total employees in database...")
        cursor.execute("SELECT COUNT(*) FROM employee")
        count = cursor.fetchone()[0]
        print(f"   Total employees in database: {count}")
        
        # Test 3: Sample existing IDs (if any)
        if count > 0:
            print("\n3. Sample existing employee IDs:")
            cursor.execute("SELECT emp_id FROM employee LIMIT 5")
            ids = cursor.fetchall()
            for emp_id_row in ids:
                print(f"   - Employee ID: {emp_id_row[0]}")
        
        cursor.close()
        db_conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Employee ID check failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_connection_pool():
    """Test connection pooling and multiple connections"""
    print("\n" + "=" * 60)
    print("CONNECTION POOL TEST")
    print("=" * 60)
    
    connections_tested = []
    
    try:
        # Test multiple consecutive connections
        for i in range(3):
            print(f"\nTesting connection {i+1}...")
            db_conn = connections.Connection(
                host=customhost,
                port=3306,
                user=customuser,
                password=custompass,
                db=customdb
            )
            
            cursor = db_conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            db_conn.close()
            
            connections_tested.append(True)
            print(f"   ✓ Connection {i+1} successful")
        
        if all(connections_tested):
            print("\n✓ All connection tests passed")
            return True
        
    except Exception as e:
        print(f"✗ Connection pool test failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("\n" + "=" * 60)
    print("EMPLOYEE MANAGEMENT SYSTEM - DIAGNOSTIC TOOL")
    print("=" * 60)
    print(f"Timestamp: {__import__('datetime').datetime.now()}")
    print()
    
    # Test 1: Database connection
    db_success = test_database_connection()
    
    if not db_success:
        print("\n" + "=" * 60)
        print("CRITICAL: Database connection failed!")
        print("=" * 60)
        print("\nPossible issues:")
        print("1. Database credentials have changed")
        print("2. Network/firewall rules blocking access")
        print("3. Database instance is not running")
        print("4. IP address restrictions on database")
        print("\nPlease check:")
        print("- Environment variables (DB_HOST, DB_USER, DB_PASS)")
        print("- AWS RDS instance status")
        print("- Security group rules")
        print("- Network connectivity")
        return
    
    # Test 2: Employee ID check
    test_employee_id_check(999999)  # Test with a random ID
    
    # Test 3: Connection pool
    test_connection_pool()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print("If all tests passed but the web interface still shows errors:")
    print("1. Check web server logs for detailed errors")
    print("2. Verify the Flask app is using the same config")
    print("3. Check if there are any recent code changes")
    print("4. Test the actual /check-emp-id endpoint via curl or browser")

if __name__ == "__main__":
    main()

