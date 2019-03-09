from django.urls import path

from .views import SaleProductFormView
from .views import TpagaPaymentDetailView

app_name = 'sales'
urlpatterns = [
    path(
        'payment/tpaga/<str:order>',
        TpagaPaymentDetailView.as_view(),
        name='tpaga_payment_details'
    ),
    path('product/', SaleProductFormView.as_view(), name='create'),
]
