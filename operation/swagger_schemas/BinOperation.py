from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

header_parameter = openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)


class BinOperationParams(object):

    def get(self):
        return swagger_auto_schema(manual_parameters=[
            header_parameter
        ])

    def post(self):
        return swagger_auto_schema(manual_parameters=[
            header_parameter
        ], request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['bin_id', 'operation_id'],
            properties={
                'bin_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                'operation_id': openapi.Schema(type=openapi.TYPE_NUMBER),
                'collection_frequency': openapi.Schema(type=openapi.TYPE_NUMBER),
                'last_collection': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ))
