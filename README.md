# Онлайн-магазин

Сервис написан в рамках самообучения. Будет дополняться.

## Функциональные возможности

- Реализовано добавление товаров на сайт
- Реализована корзина на основе сеансов Django
- Отправка электронных писем об успешном оформлении заказа посредством Celery и асинхронной задачи  
- Интегрировал платежный шлюз Stripe 
- Реализовал применение веб-перехватчиков для получения уведомлений о платежах
- Реализовал экспорт заказов в CSV файл через админку
- Реализовал просмотр заказов в формате PDF через админку, а так же автоматическую отправку письма с прикрепленным PDF файлом с данными заказа с помощью WeasyPrint
- Реализовал систему скидочных купонов 
- Реализовал рекомендательный механизм с помощью Redis
- Добавил возможность смены языка на сайте с русского на английский посредством gettext и Rosetta
- Перевёл модели с помощью django-parler
- Добавил регистрацию, вход/выход пользователя, сброс и восстановление пароля по электронной почте с помощью встроенного фреймворка аутентификации

## Стэк технологии

- Django
- PostgreSQL
- HTML/CSS
- Celery
- Redis
- RabbitMQ
- Stripe