
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import DetailView

from .forms import SaleForm
from .mixins import PaymentConfirmationMixin
from .mixins import SaleMixin
from .mixins import SaleProductMixin
from .models import TpagaPayment


def succes_view(request):
    return render(request, 'sales/succes.html')


def failure_view(request):
    return render(request, 'sales/failure.html')


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


class TpagaPaymentConfirmation(PaymentConfirmationMixin, DetailView):
    model = TpagaPayment
    template_name = 'sales/tpaga_payment_details.html'

    def get_object(self, queryset=None):
        order = self.kwargs.get('order')

        return self.model.objects.get(sale__order=order)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.status == TpagaPayment.CREATED:
            # Is necessary to confirm the payment
            return self.confirm_payment()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
