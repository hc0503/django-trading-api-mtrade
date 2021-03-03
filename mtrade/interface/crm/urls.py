from rest_framework_nested import routers

from .institution_lead.views import InstitutionLeadViewSet

CRM_PATTERN = r'crm'
INST_LEAD_PATTERN = r'institution-lead'

router = routers.SimpleRouter()

router.register(CRM_PATTERN+'/'+INST_LEAD_PATTERN, InstitutionLeadViewSet, basename=CRM_PATTERN+'/'+INST_LEAD_PATTERN)

