from django.db import models
from core.models import TimestampedModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(TimestampedModel):
    """
    Product category model
    """
    name = models.CharField(_('category name'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)
    slug = models.SlugField(_('slug'), max_length=120, unique=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(TimestampedModel):
    """
    Product model with relationship to Category
    """
    name = models.CharField(_('product name'), max_length=200)
    description = models.TextField(_('description'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(_('stock quantity'), default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name=_('category')
    )
    slug = models.SlugField(_('slug'), max_length=220, unique=True)
    image = models.ImageField(_('product image'), upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(_('is available'), default=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Order(TimestampedModel):
    """
    Order model with relationship to User
    """
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('user')
    )
    status = models.CharField(
        _('order status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_amount = models.DecimalField(_('total amount'), max_digits=10, decimal_places=2, default=0)
    shipping_address = models.TextField(_('shipping address'))
    notes = models.TextField(_('order notes'), blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"


class OrderItem(TimestampedModel):
    """
    Order item model with relationships to Order and Product
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('order')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('product')
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
        unique_together = [['order', 'product']]

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"

    def save(self, *args, **kwargs):
        # Auto-populate price from product if not set
        if not self.price and self.product:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def get_subtotal(self):
        return self.quantity * self.price
