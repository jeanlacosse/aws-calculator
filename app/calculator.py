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
    num1 = float(event['num1'])
    num2 = float(event['num2'])
    operation = event['operation']

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