from rest_framework_nested import routers

from . import views
from .cob import views as cob_views
from .rfq import views as rfq_views
from .cob.transaction.views import CobTransactionViewSet

MARKET_PATTERN = r'market'
COB_PATTERN = r'cob'
COB_TRANSACTION_PATTERN = r'transaction'
RFQ_PATTERN = r'rfq'


market_base_router = routers.SimpleRouter()
market_base_router.register(
    MARKET_PATTERN, views.MarketViewSet, basename='market')


market_subrouter = routers.NestedSimpleRouter(
    market_base_router, MARKET_PATTERN, lookup='market')
market_subrouter.register(
    COB_PATTERN, cob_views.COBViewSet, basename='market-cob')
market_subrouter.register(
    RFQ_PATTERN, rfq_views.RfqViewSet, basename='market-rfq')


market_cob_subrouter = routers.NestedSimpleRouter(
    market_subrouter, COB_PATTERN, lookup='cob_order')
market_cob_subrouter.register(
    COB_TRANSACTION_PATTERN, CobTransactionViewSet, basename='market-cob-transaction')

market_rfq_subrouter = routers.NestedSimpleRouter(
    market_subrouter, RFQ_PATTERN, lookup='rfq')
