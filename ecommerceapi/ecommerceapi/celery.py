import os
from celery import Celery

# CRITICAL: Replace 'ecommerce_api' with your ACTUAL project folder name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerceapi.settings')

app = Celery('ecommerceapi', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

# Load config from settings.py using a 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all apps
app.autodiscover_tasks()