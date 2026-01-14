# AWS Deployment Plan - Employee Management Application

## Application Overview
- **Framework**: Flask 2.3.0
- **Database**: MySQL RDS (port 3306)
- **Storage**: AWS S3 for images
- **Metadata**: DynamoDB for image URLs
- **Python Dependencies**: pymysql, boto3

## Pre-requisites on AWS EC2

### 1. Install Required Packages
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv mysql-client
```

### 2. Setup Python Virtual Environment
```bash
cd /workspaces/aws-project-1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Set these on your EC2 instance or in a `.env` file:
```bash
export DB_HOST="employee.cn8u6eqimjly.us-east-2.rds.amazonaws.com"
export DB_USER="admin"
export DB_PASS="Arjun123"
export DB_NAME="employee"
export S3_BUCKET="add-emp--123"
export AWS_REGION="us-east-2"
export FLASK_DEBUG=False
```

### 4. Configure AWS Credentials
**Option A - IAM Role (Recommended):**
- Attach IAM role to EC2 with policies for:
  - S3 read/write access to bucket `add-emp--123`
  - DynamoDB access to table `employee_image_table`

**Option B - AWS CLI:**
```bash
aws configure
# Enter access key, secret key, region, output format
```

### 5. Setup Database
```bash
mysql -h employee.cn8u6eqimjly.us-east-2.rds.amazonaws.com -u admin -p

# In MySQL shell:
CREATE DATABASE IF NOT EXISTS employee;
USE employee;
CREATE TABLE IF NOT EXISTS employee (
    emp_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    primary_skills VARCHAR(20),
    location VARCHAR(20)
);
```

### 6. Run the Application

**Development Mode:**
```bash
cd /workspaces/aws-project-1
source venv/bin/activate
python3 EmpApp.py
# Access at http://<EC2-Public-IP>/
```

**Production Mode (with Gunicorn):**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:80 EmpApp:app
```

**Production Mode (with Systemd):**
Create `/etc/systemd/system/empapp.service`:
```ini
[Unit]
Description=Employee Management Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/workspaces/aws-project-1
Environment="DB_HOST=employee.cn8u6eqimjly.us-east-2.rds.amazonaws.com"
Environment="DB_USER=admin"
Environment="DB_PASS=Arjun123"
Environment="DB_NAME=employee"
Environment="S3_BUCKET=add-emp--123"
Environment="AWS_REGION=us-east-2"
ExecStart=/workspaces/aws-project-1/venv/bin/gunicorn -w 4 -b 0.0.0.0:80 EmpApp:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable empapp
sudo systemctl start empapp
sudo systemctl status empapp
```

### 7. Configure Security Group (EC2)
- Inbound: Allow HTTP (port 80) from 0.0.0.0/0
- Outbound: Allow all traffic

### 8. Configure RDS Security Group
- Allow inbound on port 3306 from EC2 security group

## Quick Start Commands (Copy-Paste)
```bash
# 1. SSH into EC2
ssh -i your-key.pem ubuntu@<EC2-Public-IP>

# 2. Navigate and setup
cd /workspaces/aws-project-1
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv mysql-client
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run application
python3 EmpApp.py

# OR for production:
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:80 EmpApp:app
```

## Access Application
Open browser: `http://<EC2-Public-IP>`

## Troubleshooting
- Check logs: `sudo journalctl -u empapp -f`
- Test RDS connection: `mysql -h <DB_HOST> -u <DB_USER> -p`
- Verify AWS credentials: `aws sts get-caller-identity`

