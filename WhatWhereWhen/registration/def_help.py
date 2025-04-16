from django.utils import timezone
from datetime import timedelta
from .models import Users

def get_active_users():
    # Определяем временной порог для активности пользователей
    time_threshold = timezone.now() - timedelta(minutes=5)
    # Возвращаем количество пользователей, активных в последние 5 минут
    return Users.objects.filter(last_activity__gte=time_threshold).count()

