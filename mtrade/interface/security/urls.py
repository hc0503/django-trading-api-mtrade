from rest_framework import routers

from .views import SecurityView

router = routers.DefaultRouter()
# Only DRF views are placed in the router
router.register(r'security', SecurityView, basename='security')
