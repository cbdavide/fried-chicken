import uuid
from django.db import models
from django.urls import reverse

from products.models import Product
from products.models import Inventory


class Sale(models.Model):

    CASH = 10
    CREDIT_CARD = 20
    TPAGA_WALLET = 30

    PAYMENT_CHOICES = (
        (CASH, 'Cash'),
        (CREDIT_CARD, 'Credit Card'),
        (TPAGA_WALLET, 'Tpaga Wallet')
    )

    order = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )

    date = models.DateField(
        auto_now_add=True
    )

    description = models.CharField(
        blank=True,
        max_length=100,
    )

    payment_type = models.PositiveSmallIntegerField(
        choices=PAYMENT_CHOICES,
        default=TPAGA_WALLET
    )

    @property
    def total(self):
        return sum([item.subtotal for item in self.saleitem_set.all()])

    def __str__(self):
        return str(self.order)

    def get_absolute_url(self):
        return reverse('sales:detail', args=[self.id])


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveSmallIntegerField()

    @property
    def subtotal(self):
        return self.product.price_per_unit * self.quantity

    class Meta:
        unique_together = ('sale', 'product', 'inventory')


class TpagaPayment(models.Model):

    CREATED = 10
    PAID = 20
    FAILED = 30
    EXPIRED = 40
    DELIVERED = 50
    REVERTED = 60

    STATUS_CHOICES = (
        (CREATED, "Created"),
        (PAID, "Paid"),
        (FAILED, "Failed"),
        (EXPIRED, "Expired"),
        (DELIVERED, "Delivered"),
        (REVERTED, "Reverted"),
    )

    sale = models.OneToOneField(
        Sale,
        on_delete=models.CASCADE
    )

    idempotency_token = models.UUIDField(
        default=uuid.uuid4
    )

    tpaga_token = models.CharField(
        blank=True,
        max_length=100
    )

    user_ip_address = models.GenericIPAddressField()

    expires_at = models.DateTimeField()

    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=CREATED
    )

    def __str__(self):
        return str(self.sale.order)
