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
from .user.urls import router as user_router
from .market.urls import (
    router as market_router,
    cob_router as market_cob_router
)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', RedirectView.as_view(url='api/v0/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/v0/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v0/', include(user_router.urls)),
    path('api/v0/', include(security_router.urls)),
    path('api/v0/', include(market_router.urls)),
    path('api/v0/', include(market_cob_router.urls)),
    path('api/v0/schema/', SpectacularAPIView.as_view(), name='schema'),
]
