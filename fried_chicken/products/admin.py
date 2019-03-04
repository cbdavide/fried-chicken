from django.contrib import admin

from .models import Product
from .models import Inventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass
