from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import FormView

from products.models import Product
from products.util import get_items_from_inventory

from .forms import SaleForm
from .models import Sale
from .models import SaleItem
from .models import TpagaPayment


class PaymentMixin(object):

    def make_payment(self):
        information = self.process_payment()
        return HttpResponseRedirect(self.get_success_url())

    def process_payment(self):
        raise Exception("Not implemented payment method")


class TpagaPaymentMixin(PaymentMixin):
    pass

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
