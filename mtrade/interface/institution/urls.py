from rest_framework_nested import routers

from . import views
from .settlement_instruction import views as si_views

INSTITUTION_PATTERN = r'institution'
SETTLEMENT_INSTRUCTION_PATTERN = r'settlement-instruction'

router = routers.SimpleRouter()
router.register(INSTITUTION_PATTERN, views.InstitutionViewSet, basename='institution')

settlement_instruction_router = routers.NestedSimpleRouter(router, INSTITUTION_PATTERN, lookup='institution')
settlement_instruction_router.register(SETTLEMENT_INSTRUCTION_PATTERN, si_views.SettlementInstructionViewSet, basename='institution-settlement-instruction')
