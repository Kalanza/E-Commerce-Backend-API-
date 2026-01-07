from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .mpesa import MpesaClient
from ecomapi.models import Order
import json


class MpesaCheckoutView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        # Basic validation
        if not phone_number or not amount:
            return Response({"error": "Phone number and amount required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Create a Pending Order (In real life, you might already have an Order ID)
        order = Order.objects.create(
            user=request.user,
            total_amount=amount,
            shipping_address="",  # Required field - can be updated later
            is_paid=False
        )
        
        client = MpesaClient()
        try:
            # 2. Trigger M-Pesa
            response = client.make_stk_push(phone_number, amount)
            
            # 3. CRITICAL: Save the CheckoutRequestID to the Order
            # Safaricom's response looks like: {'CheckoutRequestID': 'ws_CO_...', ...}
            if 'CheckoutRequestID' in response:
                order.checkout_request_id = response['CheckoutRequestID']
                order.save()
                
            return Response(response)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MpesaCallbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        body = request.data
        
        # 1. Extract the Data
        # The structure is usually body['Body']['stkCallback']...
        stk_callback = body.get('Body', {}).get('stkCallback', {})
        
        # 2. Get the Result Code (0 = Success, anything else = Fail)
        result_code = stk_callback.get('ResultCode')
        
        # 3. Get the ID so we can find the Order
        checkout_id = stk_callback.get('CheckoutRequestID')
        
        if not checkout_id:
             return Response({"status": "failed", "message": "No ID found"})

        try:
            # 4. Find the Order
            order = Order.objects.get(checkout_request_id=checkout_id)
            
            # 5. Check if Success
            if result_code == 0:
                order.is_paid = True
                order.save()
                print(f"Order {order.id} marked as PAID!")
            else:
                print(f"Payment failed for Order {order.id}. Reason: {stk_callback.get('ResultDesc')}")
                
        except Order.DoesNotExist:
            print("Order not found for this Checkout ID")

        return Response({"status": "processed"})

