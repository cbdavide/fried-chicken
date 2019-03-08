from django import forms

from products.models import Product

from .models import Sale

SALE_QUANTITY_ITEM_MAX = 32767


class SaleForm(forms.Form):

    product = forms.ModelChoiceField(
        queryset=Product.objects.all()
    )

    quantity = forms.IntegerField(
        min_value=1,
        max_value=SALE_QUANTITY_ITEM_MAX
    )

    payment_method = forms.ChoiceField(
        choices=Sale.PAYMENT_CHOICES,
        initial=Sale.TPAGA_WALLET
    )
