from datetime import date

from django.test import TestCase

from .models import Product
from .models import Inventory

from .util import get_items_from_inventory


class GetItemsFromInventoryTest(TestCase):

    def setUp(self):

        product = Product.objects.create(
            name='test product',
            unity='test unit',
            price_per_unity=1
        )

        other_product = Product.objects.create(
            name='test other product',
            unity='test unit',
            price_per_unity=1
        )

        Inventory.objects.create(
            input_date=date(2018, 12, 1),
            product=product,
            input_quantity=10,
            current_quantity=0,
        )

        Inventory.objects.create(
            input_date=date(2019, 1, 1),
            product=product,
            input_quantity=10,
            current_quantity=5,
        )

        Inventory.objects.create(
            input_date=date(2019, 2, 1),
            product=product,
            input_quantity=20,
            current_quantity=20,
        )

    def _test_list(self, actual_response, expected_response, quantity):

        self.assertEqual(len(expected_response), len(actual_response))

        accumulated = 0
        for i in range(len(actual_response)):
            accumulated += actual_response[i]['quantity']
            self.assertEqual(expected_response[i], actual_response[i])

        self.assertEqual(accumulated, quantity)

    def test_one_inventory_needed(self):
        """It is necessary to use the unities only of one inventory."""
        quantity = 5
        product = Product.objects.get(name='test product')

        inventories = Inventory.objects.filter(
            product=product
        ).order_by('input_date')

        expected_response = [
            dict(inventory_id=inventories[1].id, quantity=5)
        ]

        actual_response = get_items_from_inventory(product, quantity)

        self._test_list(actual_response, expected_response, quantity)

    def test_two_inventories_needed(self):
        """It is necessary to use the unities of two inventories."""
        quantity = 25
        product = Product.objects.get(name='test product')

        inventories = Inventory.objects.filter(
            product=product
        ).order_by('input_date')

        expected_response = [
            dict(inventory_id=inventories[1].id, quantity=5),
            dict(inventory_id=inventories[2].id, quantity=20),
        ]

        actual_response = get_items_from_inventory(product, quantity)

        self._test_list(actual_response, expected_response, quantity)

    def test_insufficient_units(self):
        """There are not enough unities of the product to sell"""
        product = Product.objects.get(name='test product')
        other_product = Product.objects.get(name='test other product')

        with self.assertRaises(Exception):
            get_items_from_inventory(product, 26)

        with self.assertRaises(Exception):
            get_items_from_inventory(product, 100)

        with self.assertRaises(Exception):
            get_items_from_inventory(other_product, 1)
