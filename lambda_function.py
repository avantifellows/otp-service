import json
import requests
import os


def lambda_handler(event, context):
    # Base URL of Gupshup's OTP API, including all constant params
    base_URL = os.environ.get("API_BASE_URL")

    response_headers = {"Access-Control-Allow-Origin": "*"}
    event_path = str(event["path"])
    print(event_path)
    # Check for query params, otherwise return 404 (Parameters not found)
    if not event["queryStringParameters"]:
        return {
            "statusCode": 404,
            "headers": response_headers,
            "body": json.dumps("Parameters not found"),
        }

    query_params = event["queryStringParameters"]

    # Check for 'phone' param, otherwise return 404 (Phone number not found)
    if "phone" not in query_params:
        return {
            "headers": response_headers,
            "statusCode": 404,
            "body": json.dumps("Phone number not found"),
        }

    phone_number = query_params["phone"]

    # Use default values if params aren't provided
    msg = (
        query_params["msg"]
        if "msg" in query_params
        else os.environ.get("DEFAULT_OTP_MSG")
    )
    otp_code_length = (
        query_params["otpCodeLength"]
        if "otpCodeLength" in query_params
        else os.environ.get("DEFAULT_OTP_CODE_LENGTH")
    )
    otp_code_type = (
        query_params["otpCodeType"]
        if "otpCodeType" in query_params
        else os.environ.get("DEFAULT_OTP_CODE_TYPE")
    )

    # Request for OTP
    if event_path == "/sendotp":
        response = requests.post(
            base_URL,
            params={
                "phone_no": phone_number,
                "msg": msg,
                "otpCodeLength": otp_code_length,
                "otpCodeType": otp_code_type,
            },
        )

    # Verify OTP
    elif event_path == "/verifyotp":

        # Check for 'code' in params, otherwise return 404 (OTP code not found)
        if "code" not in query_params:
            return {
                "headers": response_headers,
                "statusCode": 404,
                "body": json.dumps("OTP code not found"),
            }

        response = requests.post(
            base_URL,
            params={
                "otp_code": int(query_params["code"]),
                "phone_no": phone_number,
                "msg": msg,
                "otpCodeLength": otp_code_length,
                "otpCodeType": otp_code_type,
            },
        )

    return {
        "headers": response_headers,
        "statusCode": response.status_code,
        "body": response.content,
    }
