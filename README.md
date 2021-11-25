# Avanti Fellows OTP Service

This repository contains code for sending, re-sending and verifying OTP sent to mobile numbers.

## Usage
The service is exposed in the form of two endpoints

### Send OTP
Use the below endpoint to send OTP to a mobile number.
```
https://ym6gqg7jui.execute-api.ap-south-1.amazonaws.com/dev/sendotp
```
Required query parameters: `phone`

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