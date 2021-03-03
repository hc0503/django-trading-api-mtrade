from rest_framework_nested import routers

from .views import TraderViewSet

TRADER_PATTERN = r'trader'

#SETTLEMENT_INSTRUCTION_PATTERN = r'settlement-instruction'

router = routers.SimpleRouter()
router.register(TRADER_PATTERN, TraderViewSet, basename=TRADER_PATTERN)

#settlement_instruction_router = routers.NestedSimpleRouter(router, TRADER_PATTERN, lookup=TRADER_PATTERN)

#settlement_instruction_router.register(SETTLEMENT_INSTRUCTION_PATTERN, si_views.SettlementInstructionViewSet, basename = TRADER_PATTERN + '-' + SETTLEMENT_INSTRUCTION_PATTERN)
