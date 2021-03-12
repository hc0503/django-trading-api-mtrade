from rest_framework_nested import routers

from . import views

notification_pattern = r'notification'

router = routers.SimpleRouter()
router.register(notification_pattern, views.NotificationViewSet, basename='notification')
