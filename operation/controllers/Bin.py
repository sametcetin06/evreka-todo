import datetime

from django.db.models.expressions import F, Func, Value as V
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.fields import CharField

from django.db import transaction

from navigation.logger import log, ActionType
from operation.swagger_schemas.Bin import BinParams
from operation.models import Bin


class BinController(APIView):
    route_params = BinParams()

    @route_params.get()
    def get(self, request):
        values = ['id', 'latitude', 'longitude']
        response = list(Bin.objects.all().values(*values))
        return Response({"status": True, "data": response})

    @route_params.post()
    def post(self, request):
        latitude = request.data.get('latitude', None)
        longitude = request.data.get('longitude', None)
        record = {
            "latitude": latitude,
            "longitude": longitude,
        }
        obj = Bin.objects.create(**record)
        log(request, ActionType.INSERT, obj)
        return Response({"status": True})