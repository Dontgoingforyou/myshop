from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from orders.models import Order


@shared_task
def order_created(order_id):
    """ Задание по отправке уведомления по электронной почте при успешном создании заказа """

    order = Order.objects.get(id=order_id)
    subject = f'Заказ номер {order.id}'
    message = (
        f'{order.first_name}! \n\n'
        f'Вы успешно оплатили заказ. Ваш номер заказа {order.id}'
    )
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent