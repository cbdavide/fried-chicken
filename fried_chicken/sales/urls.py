from django.urls import path

from .views import SaleFormView

urlpatterns = [
    path('product/<int:product>', SaleFormView.as_view(), name='sale_product'),
]
