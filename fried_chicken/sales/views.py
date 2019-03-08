from datetime import datetime
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic.edit import FormView
from django.views.generic import DetailView

from products.models import Product
from products.util import get_items_from_inventory

from .forms import SaleForm
from .util import create_payment_request
from .models import Sale
from .models import SaleItem
from .models import TpagaPayment


REVERSE_TPAGA_STATUS = dict(
    created=TpagaPayment.CREATED,
    paid=TpagaPayment.PAID,
    failed=TpagaPayment.FAILED,
    expired=TpagaPayment.EXPIRED,
    delivered=TpagaPayment.DELIVERED,
    reverted=TpagaPayment.REVERTED
)


class PaymentMixin(object):

    def make_payment(self):
        information = self.process_payment()
        return HttpResponseRedirect(self.get_success_url())

    def process_payment(self):
        raise Exception("Not implemented payment method")


class TpagaPaymentMixin(PaymentMixin):

    def make_payment(self):
        tpaga_payment_url = self.process_payment()
        return HttpResponseRedirect(tpaga_payment_url)

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

    def create_sale(self):

        self.sale = Sale.objects.create(
            payment_type=self.payment_type
        )

        self.sale.save()
        self.sale_items = self.create_items()

        return self.make_payment()


class SaleProductFormView(TpagaPaymentMixin, SaleProductMixin, SaleMixin, FormView):
    form_class = SaleForm
    success_url = '/sales/product'
    template_name = 'sales/sale.html'

    def get(self, request, *args, **kwargs):
        get_object_or_404(Product, pk=self.kwargs['product'])
        return super(SaleProductFormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):

        self.product = get_object_or_404(Product, pk=self.kwargs['product'])

        self.quantity = int(form.cleaned_data['quantity'])
        self.payment_type = int(form.cleaned_data['payment_method'])

        return self.create_sale()


class SaleDetailView(DetailView):
    pass
