import json
import requests

def lambda_handler(event, context):

    # Base URL of Gupshup's OTP API, including all constant params
    baseURL = "https://enterprise.smsgupshup.com/GatewayAPI/rest?userid=2000173120&password=Avanti@12345&method=TWO_FACTOR_AUTH&v=1.1&msg=%25code%25%20is%20your%20OTP%20from%20Avanti%20Fellows&format=text&otpCodeLength=4&otpCodeType=NUMERIC";

    response_headers={"Access-Control-Allow-Origin" : "*"}

    # Check for query params, otherwise return 404 (Parameters not found)
    if(event['queryStringParameters']):
        queryParams = event['queryStringParameters']

        # Check for 'phone' param, otherwise return 404 (Phone number not found)
        if('phone' not in queryParams):
            return {
            'headers': response_headers,
            'statusCode': 404,
            'body': json.dumps("Phone number not found")
            }

        phone_number = queryParams['phone']

        # Request for OTP, along with the phone number
        if(str(event['path']) == '/sendotp'):
            data = {"phone_no":phone_number}
            response = requests.post(baseURL, params=data)

        # Send OTP code for verification, along with phone number
        elif(str(event['path']) == '/verifyotp'):

            # Check for 'code' in params, otherwise return 404 (OTP code not found)
            if('code' not in queryParams):
                return {
                    'headers': response_headers,
                    'statusCode': 404,
                    'body': json.dumps("OTP code not found")
                }
            code = queryParams['code']
            data = {"otp_code":int(code), "phone_no":phone_number}
            response = requests.post(baseURL, data=data)

        return {
            'headers': response_headers,
            'statusCode': response.status_code,
            'body': response.content
        }

    return {
            'statusCode': 404,
            'headers': response_headers,
            'body': json.dumps("Parameters not found")
            }