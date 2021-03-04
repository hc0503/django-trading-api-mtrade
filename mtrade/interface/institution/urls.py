from rest_framework_nested import routers

from . import views
from .settlement_instruction import views as si_views
from .institution_manager import views as inst_manager_views
from .rfq_lock.views import RfqLockManagerViewSet

INSTITUTION_PATTERN = r'institution'

SETTLEMENT_INSTRUCTION_PATTERN = r'settlement-instruction'
INST_MANAGER_PATTERN = r'institution-manager'
RFQ_LOCK_PATTERN = r'rfq-lock'

router = routers.SimpleRouter()
router.register(INSTITUTION_PATTERN, views.InstitutionViewSet, basename=INSTITUTION_PATTERN)

settlement_instruction_router = routers.NestedSimpleRouter(router, INSTITUTION_PATTERN, lookup=INSTITUTION_PATTERN)

settlement_instruction_router.register(SETTLEMENT_INSTRUCTION_PATTERN, si_views.SettlementInstructionViewSet, basename = INSTITUTION_PATTERN + '-' + SETTLEMENT_INSTRUCTION_PATTERN)
settlement_instruction_router.register(INST_MANAGER_PATTERN, inst_manager_views.InstitutionManagerViewSet, basename= INSTITUTION_PATTERN + '-' + INST_MANAGER_PATTERN)
settlement_instruction_router.register(RFQ_LOCK_PATTERN, RfqLockManagerViewSet, basename= INSTITUTION_PATTERN + '-' + RFQ_LOCK_PATTERN)
