import json
import requests
import os
import urllib.parse


def lambda_handler(event, context):
    # Base URL of Gupshup's OTP API, including all constant params
    baseURL = os.environ.get("OTP_API_BASE_URL")
    response_headers = {"Access-Control-Allow-Origin": "*"}
    eventPath = str(event["path"])

    # Check for query params, otherwise return 404 (Parameters not found)
    if not event["queryStringParameters"]:
        return {
            "statusCode": 404,
            "headers": response_headers,
            "body": json.dumps("Parameters not found"),
        }

    queryParams = event["queryStringParameters"]

    # Check for 'phone' param, otherwise return 404 (Phone number not found)
    if "phone" not in queryParams:
        return {
            "headers": response_headers,
            "statusCode": 404,
            "body": json.dumps("Phone number not found"),
        }

    phone_number = queryParams["phone"]

    # Use default values if params aren't provided
    msg = (
        urllib.parse.quote(queryParams["msg"])
        if "msg" in queryParams
        else urllib.parse.quote(os.environ.get("DEFAULT_OTP_MSG"))
    )
    otpCodeLength = (
        queryParams["otpCodeLength"]
        if "otpCodeLength" in queryParams
        else os.environ.get("DEFAULT_OTP_CODE_LENGTH")
    )
    otpCodeType = (
        queryParams["otpCodeType"]
        if "otpCodeType" in queryParams
        else os.environ.get("DEFAULT_OTP_CODE_TYPE")
    )

    # Request for OTP, along with the phone number
    if eventPath == "/sendotp":
        response = requests.post(
            baseURL,
            params={
                "phone_no": phone_number,
                "msg": msg,
                "otpCodeLength": otpCodeLength,
                "otpCodeType": otpCodeType,
            },
        )

        # Send OTP code for verification, along with phone number
    elif eventPath == "/verifyotp":

        # Check for 'code' in params, otherwise return 404 (OTP code not found)
        if "code" not in queryParams:
            return {
                "headers": response_headers,
                "statusCode": 404,
                "body": json.dumps("OTP code not found"),
            }

        response = requests.post(
            baseURL,
            params={
                "otp_code": int(queryParams["code"]),
                "phone_no": phone_number,
                "msg": msg,
                "otpCodeLength": otpCodeLength,
                "otpCodeType": otpCodeType,
            },
        )

    return {
        "headers": response_headers,
        "statusCode": response.status_code,
        "body": response.content,
    }
