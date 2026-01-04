from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .mpesa import MpesaClient


class MpesaCheckoutView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        # Basic validation
        if not phone_number or not amount:
            return Response({"error": "Phone number and amount required"}, status=status.HTTP_400_BAD_REQUEST)
        
        client = MpesaClient()
        try:
            # Trigger the STK Push
            response = client.make_stk_push(phone_number, amount)
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MpesaCallbackView(APIView):
    # CRITICAL: Safaricom doesn't have a jwt token, so we must allow them in.
    permission_classes = [AllowAny]

    def post(self, request):
        # 1. Get the data
        body = request.data
        
        # 2. Log it(so we can see what safaricom sent us)
        print(">>>MPESA CALLBACK DATA<<<")
        print(body)

        # 3. Always return 200 OK to Safaricom (otherwise they will keep retrying)
        return Response({"status": "received"})

