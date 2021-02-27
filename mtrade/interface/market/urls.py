from rest_framework_nested import routers

from . import views
from .cob import views as cob_views

market_pattern = r'market'
cob_pattern = r'cob'

router = routers.SimpleRouter()
router.register(market_pattern, views.MarketViewSet, basename='market')

cob_router = routers.NestedSimpleRouter(router, market_pattern, lookup='market')
cob_router.register(cob_pattern, cob_views.COBViewSet, basename='market-cob')
