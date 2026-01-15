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

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("GetEmp.html")


@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skills, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql,(emp_id,))
        result = cursor.fetchone()

        if result is None:
            return render_template("GetEmpOutput.html", error=True, emp_id=emp_id)

        output["emp_id"] = result[0]
        print('EVERYTHING IS FINE TILL HERE')
        output["first_name"] = result[1]
        output["last_name"] = result[2]
        output["primary_skills"] = result[3]
        output["location"] = result[4]
        print(output["emp_id"])
        image_url = None
        dynamodb_client = boto3.client('dynamodb', region_name=customregion)
        try:
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

        except Exception as e:
            # Log the error but continue - employee data should still be shown
            print(f"Warning: Could not retrieve image URL from DynamoDB: {e}")
            # image_url remains None, employee data will still be displayed

    except Exception as e:
        print(e)
        return render_template("GetEmpOutput.html", error=True, emp_id=emp_id, error_message=str(e))

    finally:
        cursor.close()

    return render_template("GetEmpOutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"], location=output["location"],
                           image_url=image_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=os.environ.get('FLASK_DEBUG', False))
