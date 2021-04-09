from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.utils import json
from appSR.models import Numbers
from appSR.serializers import NumbersSerializer
import random


class NumbersViewSet(viewsets.ModelViewSet):
    queryset = Numbers.objects.all()
    serializer_class = NumbersSerializer


def list_number(request):
    numbers_bd = Numbers.objects.all()
    numbers = []
    for elem in numbers_bd.all():
        numbers.append(elem.value)
    return JsonResponse(numbers, safe=False)


@csrf_exempt
def generate_numbers(request):
    if request.method == "POST":
        first = json_body(request, 'first')
        last = json_body(request, 'last')
        size = json_body(request, 'size')
        list_number = []

        for i in range(size):
            number = random.randint(first, last)
            list_number.append(number)
            db_number = Numbers(value=number)
            db_number.save()

        return JsonResponse(list_number, safe=False)


###############################################################################
# ----------------------------FUNKCJE POMOCNICZE------------------------------#
###############################################################################

def json_body(request, values):
    body = json.loads(request.body)
    value = body[values]
    return value
