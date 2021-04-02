from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.utils import json
from appSR.models import Numbers
from appSR.serializers import NumbersSerializer


class NumbersViewSet(viewsets.ModelViewSet):
    queryset = Numbers.objects.all()
    serializer_class = NumbersSerializer


def list_number(request):
    numbers_bd = Numbers.objects.all()
    numbers = []
    for elem in numbers_bd.all():
        numbers.append(elem.value)
    return JsonResponse(numbers, safe=False)





###############################################################################
# ----------------------------FUNKCJE POMOCNICZE------------------------------#
###############################################################################

def json_body(request, values):
    body = json.loads(request.body)
    value = body[values]
    return value