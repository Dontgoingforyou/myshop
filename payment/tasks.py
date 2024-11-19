import weasyprint

from io import BytesIO
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order

logger = get_task_logger(__name__)

@shared_task
def payment_completed(order_id):
    """ Задание по отправке уведомления по электронной почте при успешной оплате заказа """

    try:
        order = Order.objects.get(id=order_id)

        # создание письма
        subject = f'Магазин - Счет номер {order.id}'
        message = 'Ознакомьтесь с приложенным счетом за вашу недавнюю покупку'
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])

        # генерация PDF
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

        # Прикрепление PDF к письму
        email.attach(
            f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

        email.send()
        print(f"Email отправлен: {order.email}")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


