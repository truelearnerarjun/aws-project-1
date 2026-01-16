# Security Guide

## 🔐 Security Best Practices

### 1. Environment Variables
- Never commit `.env` files to version control
- Use `.env.example` as a template
- Set strong, unique passwords and keys

### 2. AWS Security
- Use IAM roles instead of hardcoded credentials
- Enable MFA on all AWS accounts
- Use least privilege principle
- Rotate access keys regularly

### 3. Database Security
- Use strong passwords
- Enable SSL/TLS connections
- Regular backups
- Monitor access logs

### 4. Application Security
- Keep dependencies updated
- Use HTTPS in production
- Enable security headers
- Validate all inputs

## 🚨 Sensitive Files (DO NOT COMMIT)

- `config.py` - Contains actual credentials
- `.env` - Environment variables
- `*.pem`, `*.key`, `*.crt` - SSL certificates
- `aws-credentials.json` - AWS credentials
- `secrets.*` - Any secret files

## 📋 Setup Instructions

1. **Copy configuration templates:**
   ```bash
   cp config.example.py config.py
   cp .env.example .env
   ```

2. **Fill in your actual values:**
   - Edit `config.py` with your credentials
   - Edit `.env` with your environment variables

3. **Verify .gitignore:**
   ```bash
   git status
   # Should NOT show config.py or .env
   ```

4. **Test configuration:**
   ```bash
   python -c "from config import *; print('Config loaded successfully')"
   ```

## 🔍 Security Checklist

- [ ] Sensitive files in .gitignore
- [ ] Environment variables set
- [ ] Strong passwords used
- [ ] HTTPS enabled
- [ ] IAM roles configured
- [ ] Database SSL enabled
- [ ] Regular backups scheduled
- [ ] Access logging enabled

## 🛡️ Monitoring

- Monitor AWS CloudTrail for API access
- Check application logs for unusual activity
- Set up alerts for security events
- Regular security audits

## 📞 Incident Response

If credentials are compromised:
1. Immediately change all passwords
2. Rotate AWS access keys
3. Review access logs
4. Notify security team
5. Update all credentials
