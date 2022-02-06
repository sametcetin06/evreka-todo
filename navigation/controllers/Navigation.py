import datetime

from django.db.models.expressions import F, Func, Value as V
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.fields import CharField

from django.db import transaction

from navigation.logger import log, ActionType
from navigation.swagger_schemas.Navigation import NavigationParams
from navigation.models import NavigationRecord, LastNavigationRecord


class NavigationController(APIView):
    route_params = NavigationParams()

    @route_params.get()
    def get(self, request):
        annotates = {
            "vehicle_plate": F('vehicle__plate'),
            "date": Func(
                F('datetime'),
                V('DD.MM.YYYY HH24:MI:SS'),
                function='to_char',
                output_field=CharField()
            ),
        }
        values = ['vehicle_plate', 'latitude', 'longitude', 'date']
        date_filter = datetime.datetime.now() - datetime.timedelta(hours=48)
        response = list(LastNavigationRecord.objects.filter(datetime__gte=date_filter, vehicle__active=True).annotate(**annotates).order_by('-datetime').values(*values))
        return Response({"last_points": response})

    @transaction.atomic()
    @route_params.post()
    def post(self, request):
        tid = transaction.savepoint()
        try:
            vehicle_id = request.data.get('vehicle_id', None)
            latitude = request.data.get('latitude', None)
            longitude = request.data.get('longitude', None)
            record = {
                "vehicle_id": vehicle_id,
                "latitude": latitude,
                "longitude": longitude,
                "datetime": datetime.datetime.now()
            }
            # Here we save the incoming location to the database
            obj = NavigationRecord.objects.create(**record)
            log(request, ActionType.INSERT, obj)
            # If there is a previous record of this vehicle, we update it, otherwise we insert it.
            obj, created = LastNavigationRecord.objects.update_or_create(vehicle_id=vehicle_id, defaults=record)
            log(request, ActionType.INSERT, obj)
            # If there was no error during the process
            transaction.savepoint_commit(tid)
        except Exception as e:
            # In case of an error during the operation
            transaction.savepoint_rollback(tid)
            return Response({"status": False, "error": str(e)})
        return Response({"status": True})