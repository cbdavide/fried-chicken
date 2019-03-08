
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import DetailView

from .forms import SaleForm
from .mixins import SaleMixin
from .mixins import SaleProductMixin


class SaleProductFormView(SaleProductMixin, SaleMixin, FormView):
    form_class = SaleForm
    success_url = '/sales/product'
    template_name = 'sales/sale.html'

    def form_valid(self, form):

        cleaned_data = form.cleaned_data

        self.product = cleaned_data['product']

        self.quantity = int(cleaned_data['quantity'])
        self.payment_type = int(cleaned_data['payment_method'])

        return self.create_sale()


class SaleDetailView(DetailView):
    pass
