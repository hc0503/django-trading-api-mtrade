from rest_framework_nested import routers

from . import views
#from .cob import views as cob_views

INSTITUTION_PATTERN = r'institution'
#COB_PATTERN = r'cob'

router = routers.SimpleRouter()
router.register(INSTITUTION_PATTERN, views.InstitutionViewSet, basename='institution')

#cob_router = routers.NestedSimpleRouter(router, MARKET_PATTERN, lookup='market')
#cob_router.register(COB_PATTERN, cob_views.COBViewSet, basename='market-cob')
