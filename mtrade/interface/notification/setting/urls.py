from rest_framework_nested import routers

from . import views

notification_setting_pattern = r'notification/setting'

router = routers.SimpleRouter()
router.register(notification_setting_pattern, views.NotificationSettingViewSet, basename='notification_setting')
