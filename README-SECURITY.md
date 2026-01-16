# Employee Management System - Security Setup

## 🔐 Quick Security Setup

### 1. Initial Configuration

```bash
# Copy configuration templates
cp config.example.py config.py
cp .env.example .env

# Edit the files with your actual credentials
nano config.py
nano .env
```

### 2. Secure Your Credentials

**In `config.py`:**
```python
customhost = 'your-actual-rds-endpoint.rds.amazonaws.com'
customuser = 'your-actual-db-username'
custompass = 'your-actual-strong-password'
customdb = 'employee'
custombucket = 'your-unique-s3-bucket-name'
customregion = 'us-east-2'
customtable = 'emp_image_table'
```

**In `.env`:**
```bash
DB_HOST=your-actual-rds-endpoint.rds.amazonaws.com
DB_USER=your-actual-db-username
DB_PASS=your-actual-strong-password
DB_NAME=employee
S3_BUCKET=your-unique-s3-bucket-name
AWS_REGION=us-east-2
DYNAMODB_TABLE=emp_image_table
SECRET_KEY=your-very-strong-secret-key
FLASK_DEBUG=False
```

### 3. Verify Security

```bash
# Run security check
chmod +x deploy-secure.sh
./deploy-secure.sh

# Check git status (should NOT show config.py or .env)
git status
```

### 4. Deploy Securely

```bash
# Add only safe files to git
git add .
git commit -m "Add security configuration templates"
git push origin main

# Deploy to your server with secure configuration
```

## 🚨 Critical Security Rules

1. **NEVER** commit `config.py` or `.env` to git
2. **ALWAYS** use strong, unique passwords
3. **USE** HTTPS in production
4. **ENABLE** IAM roles instead of hardcoded AWS credentials
5. **ROTATE** credentials regularly

## 🔍 Security Checklist

- [ ] `config.py` contains real credentials
- [ ] `.env` contains real environment variables
- [ ] Both files are in `.gitignore`
- [ ] Git status doesn't show sensitive files
- [ ] HTTPS enabled on load balancer
- [ ] Database uses SSL/TLS
- [ ] AWS IAM roles configured
- [ ] Security groups properly configured

## 🛡️ Production Security

### AWS Security
```bash
# Enable encryption at rest
aws s3api put-bucket-encryption --bucket your-bucket --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

# Enable bucket versioning
aws s3api put-bucket-versioning --bucket your-bucket --versioning-configuration Status=Enabled

# Enable DynamoDB encryption
aws dynamodb update-table --table-name emp_image_table --specification '{"BillingMode":"PAY_PER_REQUEST","SSESpecification":{"Enabled":true,"SSEType":"KMS"}}'
```

### Database Security
```sql
-- Create secure user with limited privileges
CREATE USER 'empapp'@'%' IDENTIFIED BY 'strong-password';
GRANT SELECT, INSERT, UPDATE, DELETE ON employee.employee TO 'empapp'@'%';
FLUSH PRIVILEGES;
```

### Application Security
```python
# Add to EmpApp.py for production
from flask_talisman import Talisman

# Security headers
csp = {
    'default-src': "'self'",
    'script-src': "'self' 'unsafe-inline'cdnjs.cloudflare.com",
    'style-src': "'self' 'unsafe-inline'cdnjs.cloudflare.com",
    'img-src': "'self' data: https://*.amazonaws.com"
}

Talisman(app, force_https=True, content_security_policy=csp)
```

## 📞 Support

For security issues:
1. Check the `SECURITY.md` file
2. Run the `deploy-secure.sh` script
3. Review AWS security best practices
4. Contact your security team for production deployments

## 🔗 Additional Resources

- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)
- [Flask Security Documentation](https://flask.palletsprojects.com/en/2.3.x/security/)
- [OWASP Security Guidelines](https://owasp.org/)
