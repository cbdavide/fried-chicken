from django.urls import path

from .views import SaleFormView

app_name = 'sales'
urlpatterns = [
    path('product/<int:product>', SaleFormView.as_view(), name='create'),
]
