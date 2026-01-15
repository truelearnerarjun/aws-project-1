"""
Configuration Template - Copy to config.py and fill in your actual values
DO NOT commit the actual config.py file with real credentials!
"""

import os

# Database Configuration
customhost = os.environ.get('DB_HOST', 'your-rds-endpoint.rds.amazonaws.com')
customuser = os.environ.get('DB_USER', 'your-db-username')
custompass = os.environ.get('DB_PASS', 'your-db-password')
customdb = os.environ.get('DB_NAME', 'employee')

# AWS Configuration
custombucket = os.environ.get('S3_BUCKET', 'your-unique-bucket-name')
customregion = os.environ.get('AWS_REGION', 'us-east-2')
customtable = os.environ.get('DYNAMODB_TABLE', 'emp_image_table')

# Security Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False')

# Optional: AWS Credentials (if not using IAM roles)
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')

# Optional: Session Configuration
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SAMESITE = 'Lax'

print("Configuration loaded successfully")
