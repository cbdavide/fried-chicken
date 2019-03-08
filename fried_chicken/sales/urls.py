from django.urls import path

from .views import SaleDetailView
from .views import SaleProductFormView

app_name = 'sales'
urlpatterns = [
    path('order/<int:sale>', SaleDetailView.as_view(), name='detail'),
    path('product/', SaleProductFormView.as_view(), name='create'),
]
