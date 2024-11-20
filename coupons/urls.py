from django.urls import path

from coupons.apps import CouponsConfig
from coupons.views import coupon_apply

app_name = CouponsConfig.name

urlpatterns = [
    path('apply/', coupon_apply, name='apply'),
]