from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class SoftDeleteQuerySet(models.QuerySet):
    """
    Prevents the standard behaviour of bulk deleton.
    Example: Products.objects.filter(price__lt=10).delete()
    """
    def delete(self,hard=False):
        if hard:
            return super().delete()
        
        #Instead of deleting,we bulk update the timestamp
        return self.update(deleted_at=timezone.now())
    
class SoftDeleteManager(models.Manager):
    """
    The default manager. It hides deleted items from standard queries.
    Usage: Product.objects.all() -> returns only active items.
    """
    def get_queryset(self):
        #Always filter out soft-deleted items
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

class AllObjectsManager(models.Manager):
    """
    An extra manager to access everything(including deleted).
    Usage: Products.all_objects.all -> Returns actibve and deleted items
    """
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using =self._db)
    
class TimestampedModel(models.Model):
    """
    An abstact base class that provides self-updating 'created' and 'modified' fields, plus
    soft delete logic
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #We use a timestamp instead of a boolean
    #If it is NULL, it is active.If it has a date, it is deleted

    deleted_at = models.DateTimeField(null = True, blank =True, default =None)

    #We replace the default 'objects' manager with our custom one
    objects = SoftDeleteManager()

    #We keep a backup manager in case  we need to see deleted data  (e.g for  Admins)
    all_objects = AllObjectsManager()

    class Meta:
        abstract = True # This ensures no table is created for this model
    
    def delete(self, hard=False, **kwargs):
        """
        Overriding the standard delete method
        """
        if hard:
            # Physically remove the row from the DB
            super().delete(**kwargs)
        else:
            # Logic: Just set the flag and save
            self.deleted_at = timezone.now()
            self.save()

    def restore(self):
        """
        Helper to 'undelete' an object
        """
        self.deleted_at = None
        self.save()


  




    
