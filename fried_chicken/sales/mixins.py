from datetime import timedelta

from django.utils import timezone
from django.http import HttpResponseRedirect

from products.util import get_items_from_inventory

from .models import Sale
from .models import SaleItem
from .models import TpagaPayment
from .util import create_payment_request

REVERSE_TPAGA_STATUS = dict(
    created=TpagaPayment.CREATED,
    paid=TpagaPayment.PAID,
    failed=TpagaPayment.FAILED,
    expired=TpagaPayment.EXPIRED,
    delivered=TpagaPayment.DELIVERED,
    reverted=TpagaPayment.REVERTED
)


class PaymentHandler(object):

    def __init__(self, sale, request):
        self.sale = sale
        self.request = request

    def make_payment(self):
        information = self.process_payment()
        return HttpResponseRedirect(information)

    def process_payment(self):
        raise Exception("Not implemented payment method")


class CashPaymentHandler(PaymentHandler):
    pass


class CreditCardPaymentHandler(PaymentHandler):
    pass


class TpagaPaymentHandler(PaymentHandler):

    def process_payment(self):

        payment = TpagaPayment(
            sale=self.sale,
            user_ip_address=self.request.META['REMOTE_ADDR'],
            expires_at=timezone.now() + timedelta(days=1)
        )

        payment_information = create_payment_request(
            self.sale,
            payment
        )

        payment.tpaga_token = payment_information['token']
        payment.status = REVERSE_TPAGA_STATUS[payment_information['status']]
        payment.idempotency_token = payment_information['idempotency_token']

        payment.save()

        return payment_information['tpaga_payment_url']


class SaleProductMixin(object):

    sale = None
    product = None
    quantity = None

    def resolve_inventories(self):
        return get_items_from_inventory(self.product, self.quantity)

    def create_items(self):
        items = []
        inventories = self.resolve_inventories()

        for inventory in inventories:

            item = SaleItem(
                sale=self.sale,
                product=self.product,
                inventory=inventory['inventory'],
                quantity=inventory['quantity']
            )

            # Remove the units from the inventory
            inventory['inventory'].current_quantity -= inventory['quantity']
            inventory['inventory'].save()

            item.save()
            items.append(item)

        return items


class SaleMixin(object):
    sale = None

    def resolve_payment_handler(self):

        payment_handler_cls = TpagaPaymentHandler

        if self.payment_type == Sale.CASH:
            payment_handler_cls = CashPaymentHandler
        elif self.payment_type == Sale.CREDIT_CARD:
            payment_handler_cls = CreditCardPaymentHandler

        return payment_handler_cls

    def create_sale(self):

        self.sale = Sale.objects.create(
            payment_type=self.payment_type
        )

        self.sale.save()
        self.sale_items = self.create_items()

        payment_handler_cls = self.resolve_payment_handler()
        payment_handler = payment_handler_cls(self.sale, self.request)

        return payment_handler.make_payment()
