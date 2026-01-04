from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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