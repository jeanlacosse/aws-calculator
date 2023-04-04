import json

def add(num1, num2):
    return num1 + num2

def subtract(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

# lambda function handler
def lambda_handler(event, context):

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


