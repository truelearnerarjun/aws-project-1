from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

# Get the absolute path to the directory containing this script
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app with proper static and template paths
app = Flask(__name__, 
            static_folder=os.path.join(basedir, 'static'),
            template_folder=os.path.join(basedir, 'templates'))

# DBHOST = os.environ.get("DBHOST")
# DBPORT = os.environ.get("DBPORT")
# DBPORT = int(DBPORT)
# DBUSER = os.environ.get("DBUSER")
# DBPWD = os.environ.get("DBPWD")
# DATABASE = os.environ.get("DATABASE")

bucket= custombucket
region= customregion

db_conn = connections.Connection(
    host= customhost,
    port=3306,
    user= customuser,
    password= custompass,
    db= customdb
    
)
output = {}
table = 'employee';

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')

@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com');
@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skills = request.form['primary_skills']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']
  
    # Check if employee ID already exists
    check_sql = "SELECT emp_id FROM employee WHERE emp_id = %s"
    cursor = db_conn.cursor()
    
    try:
        cursor.execute(check_sql, (emp_id,))
        existing_emp = cursor.fetchone()
        
        if existing_emp:
            return render_template('AddEmp.html', error=True, error_message=f"Employee ID {emp_id} already exists. Please use a different ID.")
        
        insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
        
        if emp_image_file.filename == "":
            return render_template('AddEmp.html', error=True, error_message="Please select a profile image.")

        cursor.execute(insert_sql,(emp_id, first_name, last_name, primary_skills, location))
        db_conn.commit()
        emp_name = "" + first_name + " " + last_name
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-"+str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        
        
        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://{0}.s3{1}.amazonaws.com/{2}".format(
                custombucket,
                s3_location,
                emp_image_file_name_in_s3)

            # Save image file metadata in DynamoDB #
            print("Uploading to S3 success... saving metadata in dynamodb...")
        
            
            try:
                dynamodb_client = boto3.client('dynamodb', region_name='us-east-2')
                dynamodb_client.put_item(
                 TableName='emp_image_table',
                    Item={
                     'empid': {
                          'S': str(emp_id)
                      },
                      'image_url': {
                            'S': object_url
                        }
                    }
                )

            except Exception as e:
                program_msg = "Flask could not update DynamoDB table with S3 object URL"
                return str(e)
        
        except Exception as e:
            return str(e)

    except Exception as e:
        return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)

@app.route("/health", methods=['GET'])
def health_check():
    """Health check endpoint to diagnose connection issues"""
    status = {
        'database': False,
        's3': False,
        'dynamodb': False,
        'aws_credentials': False,
        'errors': []
    }
    
    # Test database
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        status['database'] = True
    except Exception as e:
        status['errors'].append(f"Database: {str(e)}")
    
    # Test AWS credentials
    try:
        sts_client = boto3.client('sts')
        sts_client.get_caller_identity()
        status['aws_credentials'] = True
    except Exception as e:
        status['errors'].append(f"AWS Credentials: {str(e)}")
    
    # Test S3
    try:
        s3_client = boto3.client('s3')
        s3_client.head_bucket(Bucket=custombucket)
        status['s3'] = True
    except Exception as e:
        status['errors'].append(f"S3: {str(e)}")
    
    # Test DynamoDB
    try:
        dynamodb = boto3.client('dynamodb', region_name=customregion)
        dynamodb.describe_table(TableName=customtable)
        status['dynamodb'] = True
    except Exception as e:
        status['errors'].append(f"DynamoDB: {str(e)}")
    
    return {
        'status': 'healthy' if all(status.values()) else 'unhealthy',
        'services': status,
        'errors': status['errors']
    }

@app.route("/check-emp-id", methods=['POST'])
def check_emp_id():
    """Check if employee ID already exists"""
    try:
        emp_id = request.form.get('emp_id', '')
        
        if not emp_id:
            return {'exists': False, 'message': 'Employee ID is required'}
        
        cursor = db_conn.cursor()
        cursor.execute("SELECT emp_id FROM employee WHERE emp_id = %s", (emp_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return {'exists': True, 'message': f'Employee ID {emp_id} already exists'}
        else:
            return {'exists': False, 'message': 'Employee ID is available'}
            
    except Exception as e:
        print(f"Error checking employee ID: {e}")
        return {'exists': False, 'message': 'Error checking employee ID'}

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("GetEmp.html")


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form.get('emp_id', '')
    print(f"Searching for employee ID: {emp_id}")

    output = {}
    image_url = None
    cursor = None
    
    try:
        select_sql = "SELECT emp_id, first_name, last_name, primary_skills, location from employee where emp_id=%s"
        
        # Test database connection
        try:
            cursor = db_conn.cursor()
            print("Database cursor created successfully")
        except Exception as db_error:
            print(f"Database connection error: {db_error}")
            return render_template("GetEmpOutput.html", error=True, emp_id=emp_id, 
                                 error_message=f"Database connection failed: {str(db_error)}")

        try:
            cursor.execute(select_sql,(emp_id,))
            result = cursor.fetchone()
            print(f"Query executed, result: {result}")

            if result is None:
                print(f"No employee found with ID: {emp_id}")
                return render_template("GetEmpOutput.html", error=True, emp_id=emp_id)

            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
            print(f"Employee data retrieved: {output}")
            
        except Exception as query_error:
            print(f"Database query error: {query_error}")
            return render_template("GetEmpOutput.html", error=True, emp_id=emp_id, 
                                 error_message=f"Database query failed: {str(query_error)}")

        # Try to get image URL from DynamoDB
        try:
            print("Attempting to retrieve image URL from DynamoDB...")
            dynamodb_client = boto3.client('dynamodb', region_name=customregion)
            
            # Try String type first (actual table schema)
            response = dynamodb_client.get_item(
                TableName=customtable,
                Key={
                    'empid': {
                        'S': str(emp_id)
                    }
                }
            )
            
            # If not found, try Number type (in case of mixed data)
            if 'Item' not in response:
                response = dynamodb_client.get_item(
                    TableName=customtable,
                    Key={
                        'empid': {
                            'N': str(emp_id)
                        }
                    }
                )
            
            if 'Item' in response and 'image_url' in response['Item']:
                image_url = response['Item']['image_url']['S']
                print(f"Image URL retrieved: {image_url}")
            else:
                print("No image URL found in DynamoDB")

        except Exception as dynamodb_error:
            # Log the error but continue - employee data should still be shown
            print(f"Warning: Could not retrieve image URL from DynamoDB: {dynamodb_error}")
            # image_url remains None, employee data will still be displayed

    except Exception as e:
        print(f"General error in FetchData: {e}")
        import traceback
        traceback.print_exc()
        return render_template("GetEmpOutput.html", error=True, emp_id=emp_id, 
                             error_message=f"Server error: {str(e)}")

    finally:
        try:
            if cursor:
                cursor.close()
                print("Database cursor closed")
        except Exception as cursor_error:
            print(f"Error closing cursor: {cursor_error}")

    print("Successfully rendering GetEmpOutput.html")
    return render_template("GetEmpOutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"],
                           image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=os.environ.get('FLASK_DEBUG', False))
