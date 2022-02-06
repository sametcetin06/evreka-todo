from django.urls import path

from operation.controllers.Bin import BinController
from operation.controllers.BinOperation import BinOperationController
from operation.controllers.Operation import OperationController

urlpatterns = [
	path('bin/', BinController.as_view(), name='bin'),
	path('operation/', OperationController.as_view(), name='operation'),
	path('binoperation/', BinOperationController.as_view(), name='binoperation'),
]