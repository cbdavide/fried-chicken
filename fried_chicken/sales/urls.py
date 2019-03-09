from django.urls import path

from .views import failure_view
from .views import SaleDetailView
from .views import SaleProductFormView
from .views import succes_view
from .views import TpagaPaymentConfirmation

app_name = 'sales'
urlpatterns = [
    path(
        'payment/confirmation/tpaga/<str:order>',
        TpagaPaymentConfirmation.as_view(),
        name='tpaga_confirmation'
    ),
    path('order/<int:sale>', SaleDetailView.as_view(), name='detail'),
    path('product/', SaleProductFormView.as_view(), name='create'),
    path('success/', succes_view, name='succes'),
    path('failure/', failure_view, name='failure'),
]
