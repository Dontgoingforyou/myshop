import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from payment.tasks import payment_completed
from shop.models import Product
from shop.recommender import Recommender


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        # Недопустимая полезная нагрузка
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Недопустимая подпись
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)

            # Пометка заказа как оплаченный
            order.paid = True

            # Сохранение id платежа stripe
            order.stripe_id = session.payment_intent
            order.save()

            # сохранение купленных позиции для рекомендации товаров
            products_ids = order.items.values_list('product_id')
            products = Product.objects.filter(id__in=products_ids)
            r = Recommender()
            r.products_bought(products)

            # Запуск асинхронного задания
            payment_completed.delay(order.id)

    return HttpResponse(status=200)