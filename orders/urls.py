from django.urls import path

from orders.apps import OrdersConfig
from orders.views import order_create

app_name = OrdersConfig.name

urlpatterns = [
    path('create/', order_create, name='order_create')
]