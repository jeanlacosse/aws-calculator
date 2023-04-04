import json
import os # this is where the environment variables from the template .yaml file are stored in a dictionary, can be used after the build
import psycopg2
import psycopg2.extras

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

# executing SQL commands to create a new table for the calculations
def create_table_if_not_exists(conn):
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS calculations (
        id SERIAL PRIMARY KEY,
        num1 NUMERIC NOT NULL,
        num2 NUMERIC NOT NULL,
        operation VARCHAR(10) NOT NULL,
        result NUMERIC NOT NULL,
        create_at TIMESTAMPTZ DEFAULT NOW()
        );
    '''

    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
        conn.commit()

# insert the calculation data into the calculations table
def insert_calculation(conn, num1, num2, operation, result): # these values are what are being placed into the % in VALUES
    insert_query = '''
        INSERT INTO calculations (num1, num2, operation, result)
        VALUES (%s, %s, %s, %s);
    '''

    with conn.cursor() as cursor:
        cursor.execute(insert_query, (num1, num2, operation, result))
        conn.commit()

# lambda function handler
def lambda_handler(event, context):

    # Retrieve environment variables
    db_host = os.environ['DB_HOST']
    db_port = os.environ['DB_PORT']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    db_name = os.environ['DB_NAME']

    # connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        dbname=db_name
    )

    # Create the 'calculations' table if it doesn't exist
    create_table_if_not_exists(conn)

    # DB operations go here
    # Insert the calculation data into the 'calculations' table
    insert_calculation(conn, num1, num2, operation, result)

    # close the database connection
    conn.close()



    # lambda test will look like this
    # {
    # "body": "{\"num1\": 5, \"num2\": 10, \"operation\": \"add\"}"
    # }
    # this is because the event object structure is different from what API gateway sends to the lambda function

    body = json.loads(event["body"]) # this is needed to format event into a dictionary as the 'body' in the JSON is unreadable otherwise. In quotes

    print( 'event is here now:', event )

    num1 = float(body["num1"])
    num2 = float(body['num2'])
    operation = body['operation']
    

    # perform operation based on input
    if operation == '+':
        result = add(num1, num2)
    elif operation == '-':
        result = subtract(num1, num2)
    elif operation == '*':
        result = multiply(num1, num2)
    elif operation == '/':
        result = divide(num1, num2)

   
    # otherwise return a 400 error
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('invalid operation')
        }
    
    
    # return result as json object
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': 'http://react-calculator-basic-client-source-code.s3-website.us-east-2.amazonaws.com',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'result': result})
    }


