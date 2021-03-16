from rest_framework_nested import routers

from . import views
from .settlement_instruction import views as si_views
from .institution_manager import views as inst_manager_views
from .rfq_lock import views as rfq_lock_views
from .institution_license import views as il_views

INST_PATTERN = r'institution'

SETTLEMENT_INSTRUCTION_PATTERN = r'settlement-instruction'
INST_MANAGER_PATTERN = r'institution-manager'
INST_LICENSE_PATTERN = r'institution-license'
RFQ_LOCK_PATTERN = r'rfq-lock'


institution_license_router = routers.SimpleRouter()
institution_license_router.register(
    INST_LICENSE_PATTERN, il_views.InstitutionLicenseSerializer, basename=INST_LICENSE_PATTERN)

institution_base_router = routers.SimpleRouter()
institution_base_router.register(
    INST_PATTERN, views.InstitutionViewSet, basename=INST_PATTERN)

institution_subrouter = routers.NestedSimpleRouter(
    institution_base_router, INST_PATTERN, lookup=INST_PATTERN
)
institution_subrouter.register(SETTLEMENT_INSTRUCTION_PATTERN, si_views.SettlementInstructionViewSet,
                               basename=INST_PATTERN + '-' + SETTLEMENT_INSTRUCTION_PATTERN)
institution_subrouter.register(
    INST_MANAGER_PATTERN, inst_manager_views.InstitutionManagerViewSet, basename=INST_PATTERN + '-' + INST_MANAGER_PATTERN)
institution_subrouter.register(
    RFQ_LOCK_PATTERN, rfq_lock_views.RfqLockViewSet, basename=INST_PATTERN + '-' + RFQ_LOCK_PATTERN)
