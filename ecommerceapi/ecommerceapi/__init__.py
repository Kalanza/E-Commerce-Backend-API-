from .celery import app as celery_app

# Make celery app available for celery -A command
celery = celery_app

__all__ = ('celery_app',)