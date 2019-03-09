from datetime import timedelta

from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

from products.util import get_items_from_inventory
from products.util import return_items_to_inventory

from .models import Sale
from .models import SaleItem
from .models import TpagaPayment
from .util import confirm_delivery
from .util import create_payment_request
from .util import confirm_payment_request

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
        try:
            information = self.process_payment()
            return HttpResponseRedirect(information)
        except NotImplementedError:
            error_message = "Sorry, the payment method is not supported yet."
        except Exception:
            error_message = "Someting went wrong, please try again in a few minutes."

        messages.error(self.request, error_message)
        return HttpResponseRedirect(reverse('sales:create'))

    def process_payment(self):
        raise NotImplementedError("Payment method not implemented")


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

        try:
            payment_information = create_payment_request(
                self.sale,
                payment
            )

            payment.tpaga_token = payment_information['token']
            payment.status = REVERSE_TPAGA_STATUS[payment_information['status']]
            payment.idempotency_token = payment_information['idempotency_token']

            payment.save()

            return payment_information['tpaga_payment_url']
        except Exception:
            return_items_to_inventory(self.sale.saleitem_set.all())
            self.sale.delete()

            raise Exception("Couldn't create the payment request.")


class SaleProductMixin(object):

    sale = None
    product = None
    quantity = None

    def product_limit_exceeded(self):
        product_name = self.product.name
        error_msg = f"Sorry, we don't have enough {product_name}s."
        messages.error(self.request, error_msg)

        # FIXME: Make the redirect more generic
        return HttpResponseRedirect(reverse('sales:create'))

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

        try:
            self.sale_items = self.create_items()

            payment_handler_cls = self.resolve_payment_handler()
            payment_handler = payment_handler_cls(self.sale, self.request)

        except Exception:
            # TODO: Add custom exceptions
            self.sale.delete()
            return self.product_limit_exceeded()

        return payment_handler.make_payment()


class PaymentConfirmationMixin(object):

    def succes(self):
        confirmation = confirm_delivery(self.object)
        status = REVERSE_TPAGA_STATUS[confirmation['status']]

        self.object.status = status
        self.object.save()

        messages.success(
            self.request,
            "The payment was successful, We'll send you your order soon."
        )

        return self.return_response()

    def failure(self):
        sale = self.object.sale

        # Returning the product units to its inventory
        return_items_to_inventory(sale.saleitem_set.all())

        messages.error(
            self.request,
            "Sorry, the payment process failed."
        )

        return self.return_response()

    def confirm_payment(self):
        confirmation = confirm_payment_request(self.object)

        status = REVERSE_TPAGA_STATUS[confirmation['status']]

        self.object.status = status
        self.object.save()

        if status == TpagaPayment.PAID:
            return self.succes()
        elif status == TpagaPayment.FAILED:
            return self.failure()

        return self.return_response()
