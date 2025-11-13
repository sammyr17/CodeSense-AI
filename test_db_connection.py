"""
Simple database connection test
"""
from database import test_database_connection, create_database_and_tables

print("🔧 Testing database connection...")
if test_database_connection():
    print("🎉 Connection successful! Creating tables...")
    if create_database_and_tables():
        print("✅ Database setup completed successfully!")
    else:
        print("❌ Failed to create tables")
else:
    print("❌ Connection failed")
    print("Make sure PostgreSQL is running and credentials are correct:")
    print("- Host: localhost")
    print("- Port: 5432") 
    print("- User: samar")
    print("- Password: admin")
    print("- Database: codesense_ai")
