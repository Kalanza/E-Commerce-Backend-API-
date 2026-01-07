import requests
import base64
from datetime import datetime
from django.conf import settings

class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.passkey = settings.MPESA_PASSKEY
        self.shortcode = settings.MPESA_SHORTCODE
        self.api_url = settings.MPESA_BASE_URL

    def get_access_token(self):
        # The URL to knock on Safaricom's door
        url = f"{self.api_url}/oauth/v1/generate?grant_type=client_credentials"

        # "Basic Auth": We show our ID(Key) and Password (Secret)
        response = requests.get(url, auth=(self.consumer_key, self.consumer_secret))

        # If they let us in (Status 200), grab the token.
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception("Failed to generate Access Token")
        
    def make_stk_push(self, phone_number, amount, account_reference="DukaTech"):
        """Triggers the STK Push popup on the user's phone."""
        access_token = self.get_access_token()
        url = f"{self.api_url}/mpesa/stkpush/v1/processrequest"

        # 1. Generate Timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # 2. Generate Password (Shortcode + Passkey + Timestamp)

        password_str = f"{self.shortcode}{self.passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount), # Sandbox requires integer amounts
            "PartyA": phone_number, # The phone sending money
            "PartyB": self.shortcode, # The paybill receiving money
            "PhoneNumber": phone_number,
            "CallBackURL": "https://ellison-ophthalmoscopic-viceregally.ngrok-free.dev/api/mpesa/callback/", #  We will fix this later
            "AccountReference": account_reference,
            "TransactionDesc": "Payment for Order"

        }

        response = requests.post(url, json=payload, headers=headers)
        return  response.json()