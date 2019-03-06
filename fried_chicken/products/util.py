
from .models import Inventory


def get_items_from_inventory(product, quantity):
    """
    Returns the needed list of inventories with the amount of units of the
    product that are going to be taken from each inventory to make a sell.
    """
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
        else:
            added = quantity - accumulated

        response_list.append(dict(
            inventory=inventory,
            quantity=added
        ))

        accumulated += added

    if accumulated != quantity:
        raise Exception('insufficient units')

    return response_list
