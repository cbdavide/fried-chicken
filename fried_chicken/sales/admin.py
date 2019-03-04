from django.contrib import admin

from .models import Sale
from .models import SaleItem
from .models import TpagaPayment


class SaleItemInline(admin.TabularInline):
    model = SaleItem

    readonly_fields = ('subtotal', )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [
        SaleItemInline,
    ]

    readonly_fields = ('order', 'total',)


@admin.register(TpagaPayment)
class TpagaPaymentAdmin(admin.ModelAdmin):
    pass
