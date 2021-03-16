"""bank_ddd_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .security.urls import router as security_router
from .security_issuer.urls import router as security_issuer_router
from .institution.urls import (
    institution_license_router,
    institution_base_router
)
from .user.urls import router as user_router
from .crm.urls import router as crm_router
from .trader.urls import (
    trader_base_router,
    trader_subrouter
)
from .market.urls import (

    market_base_router,
    market_subrouter,
    market_cob_subrouter,
    market_rfq_subrouter

)
from mtrade.infrastructure.logger.urls import urlpatterns as logger_urlpatterns
from mtrade.infrastructure.emailer.urls import urlpatterns as emailer_urlpatterns
from .notification.urls import router as notification_router
from .notification.setting.urls import router as notification_setting_router

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', RedirectView.as_view(url='api/v0/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/v0/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    # user
    path('api/v0/', include(user_router.urls)),
    # crm
    path('api/v0/', include(crm_router.urls)),
    # trader
    path('api/v0/', include(trader_base_router.urls)),
    path('api/v0/', include(trader_subrouter.urls)),
    # institution
    path('api/v0/', include(institution_base_router.urls)),
    path('api/v0/', include(institution_base_router.urls)),
    # security
    path('api/v0/', include(security_router.urls)),
    path('api/v0/', include(security_issuer_router.urls)),
    # market
    path('api/v0/', include(market_base_router.urls)),
    path('api/v0/', include(market_subrouter.urls)),
    path('api/v0/', include(market_cob_subrouter.urls)),
    path('api/v0/', include(market_rfq_subrouter.urls)),

    path('api/v0/', include(notification_router.urls)),
    path('api/v0/', include(notification_setting_router.urls)),

    path('api/v0/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v0/', include(logger_urlpatterns)),
    path('api/v0/', include(emailer_urlpatterns)),
]
