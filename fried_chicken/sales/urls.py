from django.urls import path

from .views import SaleProductFormView

app_name = 'sales'
urlpatterns = [
    path('product/<int:product>', SaleProductFormView.as_view(), name='create'),
]
