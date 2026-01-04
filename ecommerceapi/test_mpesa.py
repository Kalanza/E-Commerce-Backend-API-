import requests
import json

url = "http://127.0.0.1:8001/api/pay/"
headers = {"Content-Type": "application/json"}
data = {
    "phone_number": "254711374284", 
    "amount": 1
}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
