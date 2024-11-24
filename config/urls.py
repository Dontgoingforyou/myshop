from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.urls import path, include

from payment.webhooks import stripe_webhook

urlpatterns = i18n_patterns(
path(_('users/'), include('django.contrib.auth.urls')),
    path(_('users/'), include('users.urls', namespace='users')),
    path(_('cart/'), include('cart.urls', namespace='cart')),
    path(_('orders/'), include('orders.urls', namespace='orders')),
    path(_('payment/'), include('payment.urls', namespace='payment')),
    path(_('coupons/'), include('coupons.urls', namespace='coupons')),
    path('rosetta/', include('rosetta.urls')),
    path('', include('shop.urls', namespace='shop')),
    path(_('admin/'), admin.site.urls),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('payment/webhook/', stripe_webhook, name='stripe-webhook'),
]
