import boto3
import json
import re
from botocore.exceptions import ClientError

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def lambda_handler(event, context):
    
    # Initialize a DynamoDB client
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('BaseWaitingList')

    # Validate  parameters
    try:
        # Check if params is a string
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event
            
        user_id = body.get('user_id')
        user_email = body.get('user_email')
        user_name = body.get('user_name')

        if user_id is None:
            raise ValueError("user_id is missing")
        
        user_id = int(user_id)

        if not user_email:
            raise ValueError("user_email is missing")
        
        if not user_name:
            raise ValueError("user_name is missing")

    except (ValueError, TypeError) as e:
        return {
            'statusCode': 400,
            'headers': {
            'Access-Control-Allow-Origin': 'YOUR_LANDINGPAGE_URL',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
            'body': json.dumps(f'Invalid input: {str(e)}')
        }

    item = {
        'user_id': user_id,
        'user_email': user_email.lower(),  # Store email in lowercase
        'user_name': user_name.strip()
    }

    try:
        # Insert the item into the DynamoDB table
        response = table.put_item(
            Item=item,
            ConditionExpression='attribute_not_exists(user_id)'  # Ensure user_id doesn't already exist
        )

        # Return a success response
        return {
            'statusCode': 200,
             'headers': {
            'Access-Control-Allow-Origin': 'YOUR_LANDINGPAGE_URL',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
            'body': json.dumps('Item added successfully.')
        }
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {
                'statusCode': 409,
              'headers': {
            'Access-Control-Allow-Origin': 'YOUR_LANDINGPAGE_URL',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
                'body': json.dumps('User ID already exists.')
            }
        else:
            # Handle other ClientError exceptions
            print(f"Unexpected error: {e}")
            return {
                'statusCode': 500,
              'headers': {
            'Access-Control-Allow-Origin': 'YOUR_LANDINGPAGE_URL',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
                'body': json.dumps('Error adding item.')
            }
    except Exception as e:
        # Handle any other exceptions
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
           'headers': {
            'Access-Control-Allow-Origin': 'YOUR_LANDINGPAGE_URL',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
            'body': json.dumps('Error adding item.')
        }
        
        