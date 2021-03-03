from rest_framework import routers

from .views import SecurityIssuerViewSet

router = routers.DefaultRouter()
# Only DRF viewsets are placed in the router
router.register(r'security-issuer', SecurityIssuerViewSet, basename='security-issuer')
