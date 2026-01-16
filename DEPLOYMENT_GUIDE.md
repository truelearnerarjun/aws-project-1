# Employee Management System - Deployment Guide

## Project Overview
Employee Management System is a Flask-based web application integrated with AWS services (RDS, S3, DynamoDB) for managing employee records with profile images.

## What's New (Latest Update)

### 🎨 **Design Improvements**
- ✅ Modern, responsive UI with gradient backgrounds
- ✅ Dark mode toggle with localStorage persistence
- ✅ Font Awesome icons throughout the application
- ✅ Smooth animations and micro-interactions
- ✅ Professional navigation header with branding
- ✅ Form validation with real-time feedback
- ✅ Image preview before upload
- ✅ Breadcrumb navigation
- ✅ Toast notifications
- ✅ Fully responsive mobile design

### 📁 **Project Structure**
```
aws-project-1/
├── EmpApp.py                 # Main Flask application (NO CHANGES)
├── config.py                 # Configuration with environment variables
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── static/
│   ├── style.css            # Global stylesheet
│   └── app.js               # Shared JavaScript
└── templates/
    ├── AddEmp.html          # Add employee form
    ├── GetEmp.html          # Search employee form
    ├── AddEmpOutput.html    # Success page
    ├── GetEmpOutput.html    # Employee profile view
    └── addemperror.html     # Error page
```

## Deployment Steps

### Step 1: Prerequisites
```bash
# Install Python 3.8+
# Install pip

# Clone repository
git clone <your-repo-url>
cd aws-project-1
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file or set environment variables on your server:

```bash
# RDS Configuration
export DB_HOST="your-rds-endpoint"
export DB_USER="admin"
export DB_PASS="your-password"
export DB_NAME="employee"

# S3 Configuration
export S3_BUCKET="your-bucket-name"

# AWS Configuration
export AWS_REGION="us-east-2"

# DynamoDB Configuration
export DYNAMODB_TABLE="employee_image_table"

# Flask Configuration (optional)
export FLASK_DEBUG=False
export FLASK_ENV=production
```

### Step 4: Setup AWS Resources

**Create RDS MySQL Database:**
```sql
mysql -h <your-rds-endpoint> -u admin -p

-- Create database
CREATE DATABASE employee;
USE employee;

-- Create table
CREATE TABLE employee (
    emp_id VARCHAR(20),
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    primary_skills VARCHAR(20),
    location VARCHAR(20)
);

-- Verify table
SHOW TABLES;
DESCRIBE employee;
```

**Create S3 Bucket:**
- Go to AWS S3 Console
- Create bucket: `add-emp--1` (or your preferred name)
- Enable public read access for employee images
- Set CORS policy for file uploads

**Create DynamoDB Table:**
- Go to AWS DynamoDB Console
- Create table: `employee_image_table`
- Partition Key: `empid` (String)
- Configure billing mode (On-demand or Provisioned)

**Important Note**: The `empid` partition key must be **String type** to match the application code implementation. Using Number type will cause validation errors.

**Configure Security Groups:**
- RDS Security Group: Allow inbound traffic on port 3306 from application server IP
- S3: Configure bucket policy for public read access
- DynamoDB: Allow IAM role to access the table

### Step 5: Setup AWS Credentials
On your application server (EC2), configure AWS credentials:

```bash
# Option 1: Using AWS CLI
aws configure

# Option 2: Using IAM Role (Recommended)
# Attach IAM role to EC2 instance with S3, DynamoDB, RDS policies
```

### Step 6: Run the Application

**Development (for testing):**
```bash
python EmpApp.py
# Access at http://localhost/
```

**Production (using Gunicorn):**
```bash
# Install gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:80 EmpApp:app

# Or run with systemd service (see below)
```

### Step 7: Setup Systemd Service (Linux)
Create `/etc/systemd/system/empapp.service`:

```ini
[Unit]
Description=Employee Management Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/html/aws-project-1
Environment="DB_HOST=your-rds-endpoint"
Environment="DB_USER=admin"
Environment="DB_PASS=your-password"
Environment="DB_NAME=employee"
Environment="S3_BUCKET=add-emp--1"
Environment="AWS_REGION=us-east-2"
Environment="DYNAMODB_TABLE=employee_image_table"
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:80 EmpApp:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl enable empapp
sudo systemctl start empapp
sudo systemctl status empapp
```

### Step 8: Setup Apache/Nginx Reverse Proxy (Optional)

**Apache:**
```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
```

Create `/etc/apache2/sites-available/empapp.conf`:
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
</VirtualHost>
```

## Features

### 🎯 Frontend Features
- **Add Employee**: Form with validation and image preview
- **Search Employee**: Find employees by ID
- **View Profile**: Display employee details with image from S3
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Breadcrumb Navigation**: Easy navigation tracking
- **Form Validation**: Real-time input validation with error messages
- **Image Preview**: See image before upload

### 🔧 Backend Features
- Employee data storage in RDS MySQL
- Image upload to AWS S3
- Metadata storage in DynamoDB
- Environment variable configuration
- Error handling and logging

## Troubleshooting

### Database Connection Issues
```bash
# Test RDS connection
mysql -h <endpoint> -u admin -p -e "SELECT 1;"

# Check security group
# Ensure port 3306 is open for your application server IP
```

### S3 Upload Issues
```bash
# Verify IAM permissions
# Check bucket policy and CORS settings
# Ensure bucket name is correct
```

### Image Not Displaying
- Check S3 bucket CORS configuration
- Verify image URL in DynamoDB
- Check S3 bucket public read permissions

## Security Checklist

- ✅ Use environment variables for credentials
- ✅ Never commit `config.py` with actual values
- ✅ Use `.gitignore` for sensitive files
- ✅ Configure RDS security groups properly
- ✅ Enable HTTPS in production
- ✅ Use IAM roles instead of access keys when possible
- ✅ Regularly update dependencies

## Performance Tips

- Use RDS Read Replicas for scaling
- Enable S3 CloudFront CDN for image delivery
- Use DynamoDB Global Tables for multi-region
- Implement database connection pooling
- Add caching layer (Redis/Memcached)

## Support & Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [AWS DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)

---

**Deployment Date**: January 14, 2026
**Version**: 2.0 (Redesigned UI)
**Status**: Production Ready ✅
