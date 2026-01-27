from celery import shared_task
from django.core.mail import send_mail
from ecomapi.models import Order

@shared_task
def send_payment_success_email(order_id):
    """
    Task to send an email notification when an order is successfully paid.
    """
    print(f"--- Starting Email Task for Order {order_id} ---")
    
    try:
        # 1. Fetch the Order from the DB
        # We pass the ID, not the object, because JSON cannot store Python objects.
        order = Order.objects.get(id=order_id)
        
        # 2. Construct the Email
        subject = f'Payment Received - Order #{order.id}'
        message = f'Hi {order.user.email},\n\nWe received your payment of KES {order.total_amount}. Your order is being processed.'
        
        # 3. Send it (This prints to console because of settings.py)
        send_mail(
            subject,
            message,
            'support@dukatech.com',
            [order.user.email],
            fail_silently=False,
        )
        
        return f"Email sent successfully to {order.user.email}"
    
    except Order.DoesNotExist:
        return f"Order {order_id} not found"