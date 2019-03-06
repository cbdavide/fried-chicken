
from .models import Inventory


def get_items_from_inventory(product, quantity):

    inventories = Inventory.objects.filter(
        product=product,
        out_of_stock_date__isnull=True
    )

    inventories = inventories.order_by('input_date')

    accumulated = 0
    response_list = []

    for inventory in inventories:

        if accumulated == quantity:
            break

        added = 0

        if inventory.current_quantity < (quantity - accumulated):
            added = inventory.current_quantity
            response_list.append(dict(
                inventory_id=inventory.id,
                quantity=added
            ))
        else:
            added = quantity - accumulated
            response_list.append(dict(
                inventory_id=inventory.id,
                quantity=added
            ))

        accumulated += added

    if accumulated != quantity:
        raise Exception('insufficient units')

    return response_list
