from rest_framework_nested import routers

from .institution_lead.views import InstitutionLeadViewSet
from .concierge.views import ConciergeViewSet

CRM_PATTERN = r'crm'
INST_LEAD_PATTERN = r'institution-lead'
CONCIERGE_PATTERN = r'concierge'

router = routers.SimpleRouter()

router.register(CRM_PATTERN+'/'+INST_LEAD_PATTERN, InstitutionLeadViewSet, basename=CRM_PATTERN+'/'+INST_LEAD_PATTERN)
router.register(CRM_PATTERN+'/'+CONCIERGE_PATTERN, ConciergeViewSet, basename=CRM_PATTERN+'/'+CONCIERGE_PATTERN)
