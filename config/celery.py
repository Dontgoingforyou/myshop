import os
from celery import Celery

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Создаем приложение Celery
app = Celery('config')
# Загружаем настройки из Django
app.config_from_object('django.conf:settings', namespace='CELERY')
# Автоматическое обнаружение задач
app.autodiscover_tasks()