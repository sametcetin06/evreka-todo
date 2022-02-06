from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

header_parameter = openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)


class NavigationParams(object):

    def get(self):
        return swagger_auto_schema(manual_parameters=[
            header_parameter
        ])

    def post(self):
        return swagger_auto_schema(manual_parameters=[
            header_parameter
        ], request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['vehicle_id'],
            properties={
                'vehicle_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ))
