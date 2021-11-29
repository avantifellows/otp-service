# Avanti Fellows OTP Service

This repository contains code for sending and verifying OTP sent to mobile numbers.

## Usage
The service is exposed in the form of two endpoints.

### Send OTP
Use the below endpoint to send OTP to a mobile number.
```
https://ym6gqg7jui.execute-api.ap-south-1.amazonaws.com/dev/sendotp
```
Required query parameters: `phone`

Optional query parameters: `msg`, `otpCodeLength`, `optCodeType`

#### Example
```py
import requests
url = "https://ym6gqg7jui.execute-api.ap-south-1.amazonaws.com/dev/sendotp"
params = {
  "phone": "9999999999"
}
response = requests.post(url, params = params)
```

### Verify OTP
Use the below endpoint to verify OTP code sent to a mobile number.
```
https://ym6gqg7jui.execute-api.ap-south-1.amazonaws.com/dev/verifyotp
```
Required query parameters: `phone`, `code`

Optional query parameters: `msg`, `otpCodeLength`, `optCodeType`

#### Example
```py
import requests
url = "https://ym6gqg7jui.execute-api.ap-south-1.amazonaws.com/dev/verifyotp"
params = {
  "phone": "9999999999",
  "code":"1234"
}
response = requests.post(url, params = params)
```

### Query Parameters
`phone` : The number must be in pure numeric format with no special characters. <br/>

`msg` : The message that needs to be sent. It can contain alphanumeric & special characters. The message must contain `%code%`.
Default is `"%code% is your OTP from Avanti Fellows."` <br/>

`otpCodeLength` : This is the length of OTP. It must be a positive integer less than or equals to 10.
Default is 4. <br/>

`otpCodeType` : This parameter specifies a type of OTP. 3 values are permitted NUMERIC (only numbers), ALPHABETIC (only alphabets), ALPHANUMERIC (mix of numbers and alphabets).
Default is NUMERIC. <br/>

`code`  : The OTP code that needs to be verified.
