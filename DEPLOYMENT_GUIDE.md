# AWS Employee Database Application - React Deployment Guide

## Project Overview
- **Frontend:** React (serves via Nginx)
- **Backend:** Flask with JSON API
- **Database:** MySQL RDS
- **Storage:** S3 (for employee images)
- **Metadata:** DynamoDB
- **Notifications:** SNS (optional)
- **DNS:** Route 53 (optional)

---

## Part 1: AWS Infrastructure Setup

### Step 1-11: VPC & Security Setup ✅ (NO CHANGES)
Follow your original steps for:
- VPC: `project-vpc` (10.20.0.0/16)
- 4 Subnets (2 public, 2 private)
- Internet Gateway & NAT Gateway
- Route Tables
- Security Groups

**Security Group Rules:**
- Allow SSH (port 22) - for Bastion Host
- Allow HTTP (port 80) - for Nginx/React
- Allow HTTPS (port 443) - for future SSL
- Allow All Traffic within VPC

---

### Step 12-13: EC2 Instances ✅ (NO CHANGES)
1. **Bastion Host** (Public Subnet - public-1)
   - Ubuntu AMI
   - Auto-assign Public IP: ENABLED
   - Security Group: Allow SSH + All Traffic

2. **Application Server** (Private Subnet - private-1)
   - Ubuntu AMI
   - Auto-assign Public IP: DISABLED
   - Security Group: Allow SSH + All Traffic

---

### Step 14: Connect to Bastion Host
```bash
# From your local machine
ssh -i your-key.pem ubuntu@<bastion-public-ip>

# Copy your key pair to Bastion
scp -i your-key.pem your-key.pem ubuntu@<bastion-public-ip>:/home/ubuntu/

# Set permissions
chmod 400 your-key.pem
```

---

## Part 2: Application Server Setup (MODIFIED FOR REACT)

### Step 15: Login to Application Server & Install Dependencies

```bash
# SSH into Application Server through Bastion
ssh -i your-key.pem ubuntu@<private-app-server-ip>

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Git
sudo apt-get install git -y

# Clone repository
git clone https://github.com/zubair3337/aws-project-1.git
cd aws-project-1
ls -la
```

### Step 15a: Install MySQL Client & Python Dependencies

```bash
# MySQL Client (for RDS connection testing)
sudo apt-get install mysql-client -y

# Python 3 & Flask dependencies
sudo apt-get install python3-pip -y
pip3 install flask
pip3 install pymysql
pip3 install boto3
pip3 install flask-cors
```

### Step 15b: Install Node.js & Build React (NEW)

```bash
# Install Node.js (v18 LTS recommended)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Navigate to frontend directory
cd frontend

# Install React dependencies
npm install

# Build React for production
npm run build

# Verify build output
ls -la build/

# Return to project root
cd ..
```

### Step 15c: Install & Configure Nginx (NEW)

```bash
# Install Nginx
sudo apt-get install nginx -y

# Copy React build files to web root
sudo cp -r /home/ubuntu/aws-project-1/frontend/build/* /var/www/html/

# Create Nginx configuration file
sudo tee /etc/nginx/sites-available/default > /dev/null <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;
    root /var/www/html;
    index index.html;

    # Serve React static files
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Proxy API requests to Flask backend
    location ~ ^/(addemp|fetchdata|getemp|about)$ {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Test Nginx configuration
sudo nginx -t

# Enable and start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

### Step 16: Configure Flask Application (MODIFIED)

Update `config.py` with your AWS resources:

```bash
vim config.py
```

**config.py contents:**
```python
customhost = "your-rds-endpoint.us-east-2.rds.amazonaws.com"
customuser = "admin"
custompass = "admin123"
customdb = "employee"
custombucket = "addemp-1"
customregion = "us-east-2"
customtable = "employee_image_table"
```

### Step 16a: Update Flask App for Port 5000

```bash
vim EmpApp.py
```

Ensure the last line is:
```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)  # Changed to port 5000
```

---

### Step 17: Create S3 Bucket ✅ (NO CHANGES)

```
S3 Dashboard → Create Bucket
Name: addemp-1 (must be globally unique)
Region: us-east-2
Block Public Access: Uncheck "Block all public access"
Create Bucket
```

---

### Step 18: Create RDS Database ✅ (NO CHANGES)

**Before creating RDS:**
1. Create DB Subnet Group
   - Name: `project`
   - VPC: `project-vpc`
   - Subnets: private-1 (10.20.2.0/24) & private-2 (10.20.4.0/24)

**Create RDS Instance:**
- Engine: MySQL
- Version: 8.0
- Template: Free tier
- Master username: `admin`
- Master password: `admin123`
- VPC: `project-vpc`
- DB Subnet Group: `project`
- Public Access: NO
- Security Group: `project-sg`
- Database name: `employee`
- Database port: 3306

---

### Step 19: Create DynamoDB Table ✅ (NO CHANGES)

```
DynamoDB Dashboard → Create Table
Table name: employee_image_table
Primary key: empid (Number)
Read/Write capacity: On-demand
Create
```

---

### Step 20: Setup MySQL Database

From Application Server:
```bash
# Connect to RDS MySQL
mysql -h your-rds-endpoint.us-east-2.rds.amazonaws.com -u admin -p

# Enter password: admin123
```

In MySQL CLI:
```sql
SHOW DATABASES;
USE employee;

CREATE TABLE employee (
    emp_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(20),
    last_name VARCHAR(20),
    primary_skills VARCHAR(20),
    location VARCHAR(20)
);

SHOW TABLES;
DESCRIBE employee;
EXIT;
```

---

### Step 21: Attach IAM Role (IMPORTANT)

In AWS Console:
1. IAM → Roles → Create Role
2. Service: EC2
3. Permissions:
   - `AdministratorAccess`
   - `AmazonEC2FullAccess`
   - `AmazonRDSFullAccess`
   - `AmazonS3FullAccess`
   - `AmazonDynamoDBFullAccess`
4. Role name: `project-role`
5. Create

Attach to Application Server:
1. EC2 Dashboard → Application Server
2. Actions → Security → Modify IAM role
3. Select: `project-role`
4. Apply

---

### Step 22: Run Application Services

**Terminal 1 - Run Flask Backend:**
```bash
cd /home/ubuntu/aws-project-1
python3 EmpApp.py
# Should show: Running on http://127.0.0.1:5000/
```

**Terminal 2 - Verify Nginx is Running:**
```bash
# Verify Nginx is serving React
sudo systemctl status nginx

# Check if both services are running
netstat -tlnp | grep -E ':(80|5000)'
```

---

### Step 23: Create Application Load Balancer

1. **Create Target Group:**
   - Name: `project-app-tg`
   - Protocol: HTTP
   - Port: 80
   - VPC: `project-vpc`
   - Health checks: Path `/`
   - Register targets: Application Server

2. **Create Application Load Balancer:**
   - Name: `project-alb`
   - Scheme: Internet-facing
   - IP Address Type: IPv4
   - VPC: `project-vpc`
   - Subnets: public-1 & public-2
   - Security Group: `project-sg`
   - Listener: HTTP (80) → Target Group `project-app-tg`

3. **Get ALB DNS Name:**
   - Copy from Load Balancer details
   - Access application: `http://<alb-dns-name>`

---

### Step 24: Configure SNS Notifications (Optional)

```bash
# In AWS Console

# 1. Create SNS Topic
SNS → Create Topic
Name: employee-events
Type: Standard
Create topic

# 2. Create Subscription
Select topic → Create subscription
Protocol: Email
Endpoint: your-email@gmail.com
Create subscription

# 3. Confirm in your email

# 4. Edit Topic Access Policy
Go to topic → Edit → Access Policy
Replace with:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "SNS:Publish",
      "Resource": "arn:aws:sns:us-east-2:YOUR-ACCOUNT-ID:employee-events",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:*:*:addemp-1"
        }
      }
    }
  ]
}

# 5. Configure S3 Event Notification
S3 → addemp-1 bucket → Properties → Event notifications
Name: employee-upload-notification
Events: All object create events
Destination: SNS topic
Topic: employee-events
Save
```

---

### Step 25: Configure Route 53 (Optional - for Custom Domain)

1. **Register Free Domain:**
   - Go to freenom.com
   - Register a free domain

2. **Create Hosted Zone:**
   - Route 53 → Create Hosted Zone
   - Domain: your-domain.ml
   - Type: Public
   - Create

3. **Update Nameservers:**
   - Copy 4 NS records from Route 53
   - Go to freenom.com → Manage Domain → Management Tools → Nameservers
   - Replace with Route 53 NS records
   - Save

4. **Create A Record:**
   - Route 53 → your-domain.ml → Create Record
   - Name: www
   - Type: A
   - Alias: YES
   - Route traffic to: ALB (project-alb)
   - Routing policy: Simple
   - Create record

5. **Access Application:**
   - Open browser: `http://www.your-domain.ml`

---

## Part 3: Testing the Application

### Test Frontend
```bash
# Access via ALB DNS or custom domain
http://your-alb-dns.elb.amazonaws.com
```

**Test Add Employee:**
1. Click on "UPDATE DATABASE"
2. Fill form with employee details
3. Upload an image
4. Click "UPDATE DATABASE"
5. Should see success message
6. Employee data stored in RDS
7. Image stored in S3
8. Image URL stored in DynamoDB

**Test Get Employee:**
1. Click "GET EMPLOYEE INFORMATION"
2. Enter Employee ID
3. Click "FETCH INFO"
4. Should display employee details & image from S3

### Verify Data Storage
```bash
# Check RDS data
mysql -h your-rds-endpoint -u admin -p
USE employee;
SELECT * FROM employee;
EXIT;

# Check S3 images
# S3 Console → addemp-1 bucket → Should see emp-id-*.* files

# Check DynamoDB data
# DynamoDB Console → employee_image_table → Items
# Should see image URLs for each employee
```

---

## Part 4: Cleanup (When Done)

```bash
# In AWS Console - Delete in this order:
1. Load Balancer (project-alb)
2. Target Group (project-app-tg)
3. EC2 Instances (Bastion + App Server)
4. NAT Gateway (release Elastic IP - important!)
5. VPC (deletes subnets, routes, IGW)
6. RDS Instance (employee database)
7. S3 Bucket (addemp-1)
8. DynamoDB Table (employee_image_table)
9. SNS Topic (optional)
10. Route 53 Hosted Zone (optional)
11. IAM Role (project-role)
12. Security Groups
```

---

## Troubleshooting Guide

### Flask Backend Not Working
```bash
# SSH to app server
cd /home/ubuntu/aws-project-1

# Check if Flask is running
ps aux | grep python3

# Check Flask logs
python3 EmpApp.py

# Test Flask locally
curl http://localhost:5000/
```

### React Frontend Shows 404
```bash
# Check Nginx configuration
sudo nginx -t

# Verify React build exists
ls /var/www/html/

# Restart Nginx
sudo systemctl restart nginx
```

### Database Connection Error
```bash
# Test RDS connection
mysql -h your-rds-endpoint -u admin -p

# Update config.py with correct endpoint
vim config.py

# Restart Flask
pkill -f "python3 EmpApp.py"
python3 EmpApp.py
```

### S3 Upload Failing
- Verify IAM role has S3 full access
- Check bucket name in config.py
- Verify bucket exists and is in correct region

---

## Architecture Diagram

```
[User] 
   ↓
[Route 53 / ALB DNS]
   ↓
[Application Load Balancer] (Port 80, Public Subnets)
   ↓
[Nginx Reverse Proxy] (Port 80, App Server)
   ├→ React Build Files (Static)
   └→ Flask API (Port 5000)
        ├→ [RDS MySQL] - Employee Data
        ├→ [S3] - Employee Images
        └→ [DynamoDB] - Image URLs
             ↓
[SNS] - Email Notifications (Optional)
```

---

## Key Configuration Files

### Nginx Config Location
```
/etc/nginx/sites-available/default
```

### Flask Config Location
```
/home/ubuntu/aws-project-1/config.py
/home/ubuntu/aws-project-1/EmpApp.py
```

### React Build Location
```
/home/ubuntu/aws-project-1/frontend/build/
/var/www/html/ (served by Nginx)
```

---

## Performance & Security Notes

1. **Use Elastic IP** for NAT Gateway (prevents connection loss)
2. **Enable Auto-scaling** for production (setup auto-scaling groups)
3. **Use HTTPS** in production (AWS Certificate Manager)
4. **Monitor CloudWatch** for logs and metrics
5. **Setup CloudFront** for faster image delivery from S3
6. **Enable RDS backups** in production
7. **Use Secrets Manager** for database passwords

---

## Support & Resources

- AWS Documentation: https://docs.aws.amazon.com/
- React Docs: https://react.dev/
- Flask Docs: https://flask.palletsprojects.com/
- GitHub Repository: https://github.com/zubair3337/aws-project-1.git

---

**Last Updated:** January 11, 2026
**Status:** Ready for Deployment ✅
