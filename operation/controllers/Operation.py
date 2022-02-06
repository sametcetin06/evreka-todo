from rest_framework.response import Response
from rest_framework.views import APIView
from navigation.logger import log, ActionType
from operation.swagger_schemas.Operation import OperationParams
from operation.models import Operation


class OperationController(APIView):
    route_params = OperationParams()

    @route_params.get()
    def get(self, request):
        response = list(Operation.objects.all().values('id', 'name'))
        return Response({"status": True, "data": response})

    @route_params.post()
    def post(self, request):
        name = request.data.get('name', None)
        obj = Operation.objects.create(name=name)
        log(request, ActionType.INSERT, obj)
        return Response({"status": True})