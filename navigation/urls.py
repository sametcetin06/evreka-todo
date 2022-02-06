from django.urls import path

from navigation.controllers.Navigation import NavigationController
from navigation.controllers.Vehicle import VehicleController

urlpatterns = [
	path('vehicle/', VehicleController.as_view(), name='vehicle'),
	path('navigation/', NavigationController.as_view(), name='navigation'),
]

