from rest_framework.response import Response
from rest_framework.views import APIView

from navigation.logger import log, ActionType
from navigation.models import Vehicle
from navigation.swagger_schemas.Vehicle import VehicleParams


class VehicleController(APIView):
    route_params = VehicleParams()

    @route_params.get()
    def get(self, request):
        params = request.query_params
        id = params['id'] if 'id' in params else None
        if id:
            vehicles = Vehicle.objects.filter(id=id)
        else:
            vehicles = Vehicle.objects.filter(active=True)
        response = list(vehicles.values('id', 'plate'))
        return Response({'status': True, 'data': response})

    @route_params.post()
    def post(self, request):
        plate = request.data.get('plate', None)
        if not plate and Vehicle.objects.filter(plate=plate).exists():
            return Response({'status': False, 'error': 'Invalid license plate or vehicle registered'})
        else:
            obj = Vehicle.objects.create(plate=plate)
            log(request, ActionType.INSERT, obj)
        return Response({'status': True})

    @route_params.put()
    def put(self, request):
        id = request.POST.get('id', None)
        plate = request.POST.get('plate', None)
        vehicle = Vehicle.objects.get(id=id)
        vehicle.plate = plate
        vehicle.save()
        log(request, ActionType.UPDATE, vehicle)
        return Response({'status': True})

    @route_params.delete()
    def delete(self, request):
        id = request.POST.get('id', None)
        vehicle = Vehicle.objects.get(id=id)
        vehicle.active = False
        vehicle.save()
        log(request, ActionType.DELETE, vehicle)
        return Response({'status': True})
