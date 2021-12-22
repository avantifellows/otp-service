Avanti's OTP service uses [Gupshup's](https://www.gupshup.io/developer/home) OTP API for authentication.

This service dynamically generates a numeric/alphanumeric/alphabetical code that authenticates the user for a single transaction or session. The code or one-time password (OTP) can be sent to the user via SMS.

The API is protected, hence you need to add an API key to the header of each call. (See examples below)

The service is exposed in the form of two endpoints.

### **Send OTP**
Use the below endpoint to send OTP to a mobile number.

`https://aaxf5yvzlc.execute-api.ap-south-1.amazonaws.com/prod/sendotp`

Required query parameters: `phone`

Optional query parameters: `msg`, `otpCodeLength`, `optCodeType`

### **Example**

```python
import requests
url = "https://aaxf5yvzlc.execute-api.ap-south-1.amazonaws.com/prod/sendotp"
headers = {
	"x-api-key" : "XXXXXX"
}
params = {
  "phone": "9999999999"
}
response = requests.post(url, headers = headers, params = params)
```
### **Verify OTP**
Use the below endpoint to verify OTP code sent to a mobile number.

`https://aaxf5yvzlc.execute-api.ap-south-1.amazonaws.com/prod/verifyotp`

Required query parameters: `phone`, `code`

### **Example**

```python
import requests
url = "https://aaxf5yvzlc.execute-api.ap-south-1.amazonaws.com/prod/verifyotp"
headers = {
	"x-api-key" : "XXXXXX"
}
params = {
  "phone": "9999999999",
  "code":"1234"
}
response = requests.post(url, headers = headers, params = params)
```

### **Query Parameters**

`phone` : The number must be in pure numeric format with no special characters.

`msg` : The message that needs to be sent. It can contain alphanumeric & special characters. The message must contain `%code%`. Default is `"%code% is your OTP from Avanti Fellows."`

`otpCodeLength` : This is the length of OTP. It must be a positive integer less than or equals to 10. Default is 4.

`otpCodeType` : This parameter specifies a type of OTP. 3 values are permitted NUMERIC (only numbers), ALPHABETIC (only alphabets), ALPHANUMERIC (mix of numbers and alphabets). Default is NUMERIC.

`code` : The OTP code that needs to be verified.
