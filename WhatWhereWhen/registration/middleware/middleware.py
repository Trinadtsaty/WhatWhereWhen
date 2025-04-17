from django.utils import timezone
from django.contrib.sessions.models import Session


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Обновляем время последней активности пользователя
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])

        response = self.get_response(request)
        return response

# class GiveAchievementsMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Обновляем время последней активности пользователя
#         if request.user.is_authenticated:
#             request.user.last_activity = timezone.now()
#             request.user.save(update_fields=['last_activity'])
#
#         response = self.get_response(request)
#         return response