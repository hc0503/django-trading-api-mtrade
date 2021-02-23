from rest_framework import routers

from .views import SecurityViewSet

router = routers.DefaultRouter()
# Only DRF viewsets are placed in the router
router.register(r'security', SecurityViewSet, basename='security')
