from django.views.generic.edit import FormView

from .forms import SaleForm


class SaleFormView(FormView):
    template_name = 'sales/sale.html'
    form_class = SaleForm
    success_url = '/sales/product'
