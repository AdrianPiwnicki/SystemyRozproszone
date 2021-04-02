from rest_framework import viewsets
from rest_framework.utils import json
from appSR.models import Numbers
from appSR.serializers import NumbersSerializer


class NumbersViewSet(viewsets.ModelViewSet):
    queryset = Numbers.objects.all()
    serializer_class = NumbersSerializer


###############################################################################
# ----------------------------FUNKCJE POMOCNICZE------------------------------#
###############################################################################

def json_body(request, values):
    body = json.loads(request.body)
    value = body[values]
    return value