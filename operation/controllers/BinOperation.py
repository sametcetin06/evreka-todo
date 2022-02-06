import datetime

from rest_framework.views import APIView
from operation.models import BinOperation
from rest_framework.response import Response
from navigation.logger import log, ActionType
from django.db.models.fields import CharField
from django.db.models.expressions import F, Value as V, Func
from operation.swagger_schemas.BinOperation import BinOperationParams


class BinOperationController(APIView):
    route_params = BinOperationParams()

    @route_params.get()
    def get(self, request):
        annotates = {
            'latitude': F('bin__latitude'),
            'longitude': F('bin__longitude'),
            'operation_name': F('operation__name'),
            "date": Func(
                F('last_collection'),
                V('DD.MM.YYYY HH24:MI:SS'),
                function='to_char',
                output_field=CharField()
            ),
        }
        values = ['bin_id', 'operation_id', 'latitude', 'longitude', 'operation_name', 'collection_frequency', 'date']
        response = list(BinOperation.objects.all().annotate(**annotates).values(*values))
        return Response({"status": True, "data": response})

    @route_params.post()
    def post(self, request):
        # Here is where the collection_frequency and last_collection data for bin and operations are saved.
        # This operation could also be done in operation or bin. This administration was chosen for clarity.
        operation_id = request.data.get('operation_id', None)
        bin_id = request.data.get('bin_id', None)
        collection_frequency = request.data.get('collection_frequency', 0)
        last_collection = request.data.get('last_collection', None)
        last_collection = datetime.datetime.strptime(last_collection, '%Y-%m-%d %H:%M:%S') if last_collection else datetime.datetime.now()
        obj = BinOperation.objects.create(
            bin_id=bin_id,
            operation_id=operation_id,
            collection_frequency=collection_frequency,
            last_collection=last_collection
        )
        log(request, ActionType.INSERT, obj)
        return Response({"status": True})