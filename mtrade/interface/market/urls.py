from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter()
router.register(r'market', views.MarketViewSet)
