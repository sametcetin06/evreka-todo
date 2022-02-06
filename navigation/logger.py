from django.utils import timezone
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from navigation.models import Log
import django.dispatch

event_logged = django.dispatch.Signal(providing_args=["event"])


class ActionType:
    INSERT = 'INSERT'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    CHECK = 'CHECK'
    UNCHECK = 'UNCHECK'
    PASSIVE = 'PASSIVE'
    ACTIVE = 'ACTIVE'


ACTION_TYPE = (
    (ActionType.INSERT, 'INSERT'),
    (ActionType.UPDATE, 'UPDATE'),
    (ActionType.DELETE, 'DELETE'),
    (ActionType.CHECK, 'CHECK'),
    (ActionType.UNCHECK, 'UNCHECK'),
    (ActionType.PASSIVE, 'PASSIVE'),
    (ActionType.ACTIVE, 'ACTIVE')
)

# Customization for ip_address field.
# List of HTTP headers where we will search user IP
IP_ADDRESS_HEADERS = ('HTTP_X_REAL_IP', 'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR')


def get_ip_address(request):
    for header in IP_ADDRESS_HEADERS:
        addr = request.META.get(header)
        if addr:
            return addr.split(',')[0].strip()


def log(request, action, obj=None, extra=None, dateof=None):
    try:
        user = request.user.id
    except AttributeError:
        user = None
        extra = extra if extra else 'Cronjob'

    content_type = None
    object_id = None
    if obj is not None:
        content_type = ContentType.objects.get_for_model(obj)
        object_id = obj.pk

    if dateof is None:
        dateof = timezone.now()

    data = None
    if action == ActionType.INSERT:
        data = serializers.serialize('json', [obj, ]),
    elif action == ActionType.UPDATE:
        data = {}
        data['model'] = content_type.app_label + "." + content_type.model
        data['pk'] = obj.pk
        data = str(data)
    elif action == ActionType.DELETE:
        data = serializers.serialize('json', [obj, ]),

    try:
        request_method = "AJAX_" + request.method if request.is_ajax() else request.method
        request_path = request.path
        ip_address = get_ip_address(request)
    except AttributeError:
        request_method = None
        request_path = None
        ip_address = None

    event = Log.objects.create(
        user_id=user,
        action=action,
        content_type=content_type,
        object_id=object_id,
        data=data,
        extra=str(extra) if extra is not None else '',
        timestamp=dateof,
        request_url=request_path,
        ip_address=ip_address,
        request_method=request_method,
    )
    event_logged.send(sender=Log, event=event)
    return event
