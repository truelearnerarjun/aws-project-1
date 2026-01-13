import os

customhost = os.environ.get('DB_HOST', 'employee.cn8u6eqimjly.us-east-2.rds.amazonaws.com')
customuser = os.environ.get('DB_USER', 'admin')
custompass = os.environ.get('DB_PASS', '')
customdb = os.environ.get('DB_NAME', 'employee')
custombucket = os.environ.get('S3_BUCKET', 'add-emp--123')
customregion = os.environ.get('AWS_REGION', 'us-east-2')
customtable = os.environ.get('DYNAMODB_TABLE', 'emp_image_table')
