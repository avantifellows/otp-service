import boto3
import json
import random
from datetime import datetime, timedelta

def lambda_handler(event, context):
    try:
        # Determine endpoint based on path
        path = event.get('path', '')
        
        if path == '/sendotp':
            return send_otp(event)
        elif path == '/verifyotp':
            return verify_otp(event)
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def send_otp(event):
    try:
        # Get phone number from query params
        phone_number = event['queryStringParameters']['phone']
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Store OTP in DynamoDB with 2-minute expiry
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('portal_otp_table')
        
        expiry_time = datetime.now() + timedelta(minutes=2)
        
        table.put_item(Item={
            'phone_number': phone_number,
            'otp': otp,
            'expiry_time': int(expiry_time.timestamp()),
            'attempts': 0,
            'created_at': int(datetime.now().timestamp())
        })
        
        # Send SMS via SNS
        sns = boto3.client('sns', region_name='ap-south-1')
        
        message = f"Your Avanti OTP is: {otp}. Valid for 2 minutes. Do not share with anyone."
        
        response = sns.publish(
            PhoneNumber=f"+91{phone_number}",
            Message=message
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST'
            },
            'body': json.dumps({'message': 'success'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'failure', 'error': str(e)})
        }

def verify_otp(event):
    try:
        phone_number = event['queryStringParameters']['phone']
        submitted_otp = event['queryStringParameters']['code']
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('portal_otp_table')
        
        # Get OTP record
        response = table.get_item(Key={'phone_number': phone_number})
        
        if 'Item' not in response:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'statusCode': 311})  # OTP doesn't exist
            }
        
        item = response['Item']
        
        # Check if expired
        current_time = int(datetime.now().timestamp())
        if current_time > item['expiry_time']:
            table.delete_item(Key={'phone_number': phone_number})
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'statusCode': 301})  # OTP expired
            }
        
        # Check attempts
        if item['attempts'] >= 3:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'statusCode': 309})  # Too many attempts
            }
        
        # Check if correct OTP
        if item['otp'] == submitted_otp:
            # Success - delete OTP
            table.delete_item(Key={'phone_number': phone_number})
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'statusCode': 200})  # Success
            }
        else:
            # Increment attempts
            table.update_item(
                Key={'phone_number': phone_number},
                UpdateExpression='SET attempts = attempts + :val',
                ExpressionAttributeValues={':val': 1}
            )
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'statusCode': 310})  # Wrong OTP
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'statusCode': 500, 'error': str(e)})
        }
