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
   
    num1 = float(body["num1"])
    num2 = float(body['num2'])
    operation = body['operation']
    

    # perform operation based on input
    if operation == 'add':
        result = add(num1, num2)
    elif operation == 'subtract':
        result = subtract(num1, num2)
    elif operation == 'multiply':
        result = multiply(num1, num2)
    elif operation == 'divide':
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
        'body': json.dumps(result)
    }