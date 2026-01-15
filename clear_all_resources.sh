#!/bin/bash

# Employee Management System - Resource Cleanup Script
# This script clears all data from RDS, DynamoDB, and S3

echo "🗄️  Clearing Employee Management System Resources..."
echo "================================================"

# Configuration from config.py
DB_HOST="employee.cn8u6eqimjly.us-east-2.rds.amazonaws.com"
DB_USER="admin"
DB_PASS="Arjun123"
DB_NAME="employee"
S3_BUCKET="add-emp--123"
DYNAMO_TABLE="emp_image_table"
AWS_REGION="us-east-2"

echo "📊 Configuration:"
echo "  RDS Host: $DB_HOST"
echo "  Database: $DB_NAME"
echo "  S3 Bucket: $S3_BUCKET"
echo "  DynamoDB Table: $DYNAMO_TABLE"
echo "  Region: $AWS_REGION"
echo ""

# Clear RDS Employee Table
echo "🗄️  Clearing RDS employee table..."
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS -e "USE $DB_NAME; DELETE FROM employee; SELECT COUNT(*) AS 'Remaining Records' FROM employee;"
if [ $? -eq 0 ]; then
    echo "✅ RDS table cleared successfully"
else
    echo "❌ Failed to clear RDS table"
fi
echo ""

# Clear DynamoDB Table
echo "🔥 Clearing DynamoDB table..."
aws dynamodb delete-table --table-name $DYNAMO_TABLE --region $AWS_REGION
echo "Waiting for table deletion..."
aws dynamodb wait table-not-exists --table-name $DYNAMO_TABLE --region $AWS_REGION

aws dynamodb create-table \
    --table-name $DYNAMO_TABLE \
    --attribute-definitions AttributeName=empid,AttributeType=S \
    --key-schema AttributeName=empid,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $AWS_REGION

echo "Waiting for table creation..."
aws dynamodb wait table-exists --table-name $DYNAMO_TABLE --region $AWS_REGION

if [ $? -eq 0 ]; then
    echo "✅ DynamoDB table recreated successfully"
else
    echo "❌ Failed to recreate DynamoDB table"
fi
echo ""

# Empty S3 Bucket
echo "🪣 Emptying S3 bucket..."
aws s3 rm s3://$S3_BUCKET --recursive --region $AWS_REGION

if [ $? -eq 0 ]; then
    echo "✅ S3 bucket emptied successfully"
else
    echo "❌ Failed to empty S3 bucket"
fi
echo ""

echo "🎉 Resource cleanup completed!"
echo "All application data has been cleared."
echo ""
echo "📝 Next Steps:"
echo "1. Restart your Flask application"
echo "2. Test adding new employees"
echo "3. Verify all AWS services are working"
