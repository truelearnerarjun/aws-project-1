#!/bin/bash

# Secure Deployment Script
# This script helps deploy the application securely

echo "🔐 Starting Secure Deployment..."

# Check if sensitive files exist
if [ -f "config.py" ]; then
    echo "✅ config.py found"
else
    echo "❌ config.py not found. Please copy config.example.py to config.py"
    exit 1
fi

if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "❌ .env file not found. Please copy .env.example to .env"
    exit 1
fi

# Check git status for sensitive files
echo "🔍 Checking git status..."
git status --porcelain | grep -E "(config\.py|\.env)" && {
    echo "❌ Sensitive files are being tracked by git!"
    echo "Please run: git rm --cached config.py .env"
    exit 1
}

# Verify .gitignore has sensitive files
if grep -q "config.py" .gitignore && grep -q ".env" .gitignore; then
    echo "✅ Sensitive files are in .gitignore"
else
    echo "❌ Sensitive files not in .gitignore"
    exit 1
fi

# Check environment variables
echo "🔍 Checking environment variables..."
source .env

if [ -z "$DB_HOST" ] || [ "$DB_HOST" = "your-rds-endpoint.rds.amazonaws.com" ]; then
    echo "❌ Please update DB_HOST in .env"
    exit 1
fi

if [ -z "$DB_USER" ] || [ "$DB_USER" = "your-db-username" ]; then
    echo "❌ Please update DB_USER in .env"
    exit 1
fi

if [ -z "$DB_PASS" ] || [ "$DB_PASS" = "your-db-password" ]; then
    echo "❌ Please update DB_PASS in .env"
    exit 1
fi

echo "✅ Environment variables configured"

# Test configuration
echo "🧪 Testing configuration..."
python3 -c "
try:
    from config import *
    print('✅ Configuration loaded successfully')
    print(f'DB Host: {customhost}')
    print(f'DB Name: {customdb}')
    print(f'S3 Bucket: {custombucket}')
    print(f'AWS Region: {customregion}')
except Exception as e:
    print(f'❌ Configuration error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Configuration test passed"
else
    echo "❌ Configuration test failed"
    exit 1
fi

echo "🚀 Ready for secure deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Deploy to your server"
echo "2. Set up HTTPS with SSL certificates"
echo "3. Configure security groups"
echo "4. Enable monitoring and logging"
echo ""
echo "🔐 Security reminders:"
echo "- Never commit sensitive files to git"
echo "- Use IAM roles instead of hardcoded credentials"
echo "- Enable HTTPS in production"
echo "- Regular security audits"
