from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

header_parameter = openapi.Parameter('Authorization', openapi.IN_HEADER, type=openapi.TYPE_STRING)


class OperationParams(object):

    def get(self):
        return swagger_auto_schema(manual_parameters=[
            header_parameter
        ])

    def post(self):
        return swagger_auto_schema(manual_parameters=[
            header_parameter
        ], request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            # , 'collection_frequency', 'last_collection'
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            },
            #     ,
            #                 'collection_frequency': openapi.Schema(type=openapi.TYPE_NUMBER),
            #                 'last_collection': openapi.Schema(type=openapi.TYPE_STRING),
            #                 'bins': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
        ))
