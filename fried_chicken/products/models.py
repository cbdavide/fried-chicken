from django.db import models
from django.utils import timezone


class Product(models.Model):

    name = models.CharField(
        max_length=20
    )

    description = models.CharField(
        blank=True,
        max_length=100,
    )

    unity = models.CharField(
        max_length=20
    )

    price_per_unity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - ${self.price_per_unity}"


class Inventory(models.Model):

    input_date = models.DateField()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    input_amount = models.PositiveSmallIntegerField()

    current_amount = models.PositiveSmallIntegerField()

    out_of_stock_date = models.DateField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.current_amount == 0 and self.out_of_stock_date is None:
            # The inventory record ran out product
            self.out_of_stock_date = timezone.now().date()
        elif self.current_amount > 0 and self.out_of_stock_date is not None:
            # In case some amount of products go back to the inventory
            self.out_of_stock_date = None

        super().save(*args, **kwargs)

    def __str__(self):
        data = self.input_date.strftime('%d/%b/%Y')
        return f"{data} - {self.product.name}"

    class Meta:
        order_with_respect_to = 'input_date'
        unique_together = ('input_date', 'product')
        verbose_name_plural = "Inventories"
