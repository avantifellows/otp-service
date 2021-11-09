import json
import requests

def lambda_handler(event, context):
    
    headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json", "apikey": "f7691a013e6c4532c5ba2ceaf35eea8c"}
    otp_auth_key = "8c28c30eeeafb174daba3635a003d68c"

    if(event['queryStringParameters']):
        if('phone' not in event['queryStringParameters']):
            return {
            'statusCode': 404,
            'body': json.dumps("Phone number not found")
            }
        phone_number = event['queryStringParameters']['phone']
        
        if(str(event['path']) == '/sendotp'):
            data = {"key":otp_auth_key, "phone":phone_number}
            response = requests.post("https://api.gupshup.io/sm/api/ent/sms/2fa/sendOTP", headers=headers, data=data)
            if(response.json()['code'] == "100"):
                return {
                'statusCode': 200,
                'body': "Success. New code generated and code was sent the user."
                }
            else:
                return {
                'statusCode': 500,
                'body': "Internal server error."
                }
        elif(str(event['path']) == '/updateotp'):
            data = {"key":otp_auth_key, "message":"Resent OTP %code%"}
            response = requests.post("https://api.gupshup.io/sm/api/ent/sms/2fa/updateMessage", headers=headers, data=data)
            if(response.json()['code'] == "200"):
                return {
                'statusCode': 200,
                'body': "Success. Code resent to the user."
                }
            else:
                return {
                'statusCode': 500,
                'body': "Internal server error."
                }
        elif(str(event['path']) == '/verifyotp'):
            if('code' not in event['queryStringParameters']):
                return {
                    'statusCode': 404,
                    'body': json.dumps("OTP code not found")
                }
            code = event['queryStringParameters']['code']
            data = {"key":otp_auth_key, "phone":phone, "code":code}
            response = requests.post("https://api.gupshup.io/sm/api/ent/sms/2fa/verifyOTP", headers=headers, data=data)
            if(response.json()['code'] == "200"):
                return {
                'statusCode': 200,
                'body': "Success. User verified."
                }
            elif(response.json()['code'] == "903"):
                return {
                'statusCode': 401,
                'body': "Invalid code."
                }
            elif(response.json()['code'] == "907"):
                return {
                'statusCode': 401,
                'body': "Code is expired."
                }
            else:
                return {
                'statusCode': 500,
                'body': "Internal server error."
                }
    return {
            'statusCode': 404,
            'body': json.dumps("Parameters not found")
            }