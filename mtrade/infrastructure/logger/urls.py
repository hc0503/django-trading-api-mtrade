# django import
from django.urls import path
from rest_framework import routers

# local import
# from .views import LoggerViewSet

# local imports
from . import views

router = routers.DefaultRouter()
router.register(r'loggers', views.LoggerViewSet)