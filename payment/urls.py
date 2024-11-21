from django.urls import path
from django.utils.translation import gettext_lazy as _
from payment.apps import PaymentConfig
from payment.views import payment_process, payment_completed, payment_canceled
from payment.webhooks import stripe_webhook

app_name = PaymentConfig.name

urlpatterns = [
    path(_('process/'), payment_process, name='process'),
    path(_('completed/'), payment_completed, name='completed'),
    path(_('canceled/'), payment_canceled, name='canceled'),
]