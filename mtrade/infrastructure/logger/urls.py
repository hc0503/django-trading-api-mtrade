# django import
from django.urls import path

# local imports
from . import views

urlpatterns = [
	path('loggers/debug', views.debugLogger),
	path('loggers/info', views.infoLogger),
	path('loggers/warning', views.warningLogger),
	path('loggers/error', views.errorLogger),
	path('loggers/fatal', views.fatalLogger),
]
