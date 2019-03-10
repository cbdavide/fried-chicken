from django.contrib import admin
from django.contrib import messages

from .mixins import REVERSE_TPAGA_STATUS
from .models import Sale
from .models import SaleItem
from .models import TpagaPayment
from .util import revert_payment


class SaleItemInline(admin.TabularInline):
    model = SaleItem


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    inlines = [
        SaleItemInline,
    ]


@admin.register(TpagaPayment)
class TpagaPaymentAdmin(admin.ModelAdmin):
    change_form_template = 'sales/payment_edit_view.html'

    def response_change(self, request, obj):

        if "refund" in request.POST:

            response = revert_payment(obj)
            print(response)

            error = response.get('error_code', None)
            if error:
                messages.error(request, response['error_message'])
            else:
                object.status = REVERSE_TPAGA_STATUS[response['status']]
                objects.save()

                messages.success('The payment status changed.')

        return super().response_change(request, obj)
