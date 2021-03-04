from rest_framework_nested import routers

from .views import TraderViewSet
from .rfq_auto_responder.views import RfqAutoResponderViewSet

TRADER_PATTERN = r'trader'
RFQ_AUTO_RESPONDER_PATTERN = r'rfq-auto-responder'

trader_base_router = routers.SimpleRouter()
trader_base_router.register(TRADER_PATTERN, TraderViewSet, basename=TRADER_PATTERN)

trader_subrouter = routers.NestedSimpleRouter(trader_base_router, TRADER_PATTERN, lookup=TRADER_PATTERN)

trader_subrouter.register(RFQ_AUTO_RESPONDER_PATTERN, RfqAutoResponderViewSet, basename = TRADER_PATTERN + '-' + RFQ_AUTO_RESPONDER_PATTERN)
