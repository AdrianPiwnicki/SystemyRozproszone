import threading
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.utils import json
from appSR.models import Numbers, UserSystem, UserNumbers
from appSR.serializers import NumbersSerializer, UserSystemSerializer
import random
import time
from concurrent.futures import ThreadPoolExecutor

przebieg = ""


class NumbersViewSet(viewsets.ModelViewSet):
    queryset = Numbers.objects.all()
    serializer_class = NumbersSerializer


@csrf_exempt
def log_user(request):
    if request.method == "POST":
        name = json_body(request, 'name')
        hash = json_body(request, 'hash')
        queryset = UserSystem.objects.filter(name=name)

        if hash == 0:
            if not queryset:
                user = UserSystem(name=name, hash=1)
                user.save()
                answer = {'numbers': [], 'hash': 1}

            else:
                max_hash = queryset.order_by('-hash')[0]
                user = UserSystem(name=name, hash=max_hash.hash + 1)
                user.save()
                answer = {'numbers': [], 'hash': max_hash.hash + 1}
        else:

            if UserSystem.objects.filter(name=name, hash=hash):
                user = UserSystem.objects.filter(name=name, hash=hash)[0]
                user_numbers = UserNumbers.objects.filter(userID_id=user.id)
                user_number_list = []
                for i in user_numbers:
                    user_number_list.append(i.value)
                answer = {'numbers': user_number_list, 'hash': hash}
            else:
                answer = {'numbers': [], 'hash': 0}

        return JsonResponse(answer, safe=False)


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
        name = json_body(request, 'name')
        hash = json_body(request, 'hash')
        generated_numbers = []

        user = UserSystem.objects.filter(name=name, hash=hash)[0]

        # Numbers.objects.all().delete()

        for i in range(int(size)):
            gen_number = generator(first, last, user.id)
            generated_numbers.append(gen_number)

        return JsonResponse(generated_numbers, safe=False)


def bubble_sort(request):
    if request.method == "GET":
        queryset = Numbers.objects.all()
        bubble_list = []
        for i in queryset:
            bubble_list.append(i.value)

        n = len(bubble_list)

        t0 = time.time()
        while n > 1:
            zamien = False
            for i in range(0, n - 1):

                if bubble_list[i] > bubble_list[i + 1]:
                    bubble_list[i], bubble_list[i + 1] = bubble_list[i + 1], bubble_list[i]
                    zamien = True

            n -= 1
            if not zamien:
                break

        t1 = time.time()

        bubble_dict = {'bubbleSort': bubble_list, 'time': round((t1 - t0) * 1000, 2)}
        return JsonResponse(bubble_dict, safe=False)


def quick_sort_notthreading(request):
    if request.method == "GET":
        queryset = Numbers.objects.all()
        quick_list = []
        for i in queryset:
            quick_list.append(i.value)

        t0 = time.time()
        quicksorted = quicksort(quick_list, 0, len(quick_list) - 1)
        t1 = time.time()

        print(quick_list)
        quick_dict = {'quickSort': quicksorted, 'time': round((t1 - t0) * 1000, 2)}
        return JsonResponse(quick_dict, safe=False)


def quick_sort_multithreading(request):
    if request.method == "GET":
        queryset = Numbers.objects.all()
        quick_list = []
        for i in queryset:
            quick_list.append(i.value)

        t0 = time.time()
        global przebieg
        quicksorted = quicksort_multi(quick_list, 0, len(quick_list) - 1, 1)
        print(quicksorted)
        t1 = time.time()

        quick_dict = {'quickSort': quicksorted, 'time': round((t1 - t0) * 1000, 2), 'multithreading': przebieg}
        przebieg = ""
        return JsonResponse(quick_dict, safe=False)


###############################################################################
# ----------------------------FUNKCJE POMOCNICZE------------------------------#
###############################################################################

def json_body(request, values):
    body = json.loads(request.body)
    value = body[values]
    return value


def generator(first, last, user):
    number = random.randint(first, last)
    db_number = Numbers(value=number)
    db_user_number = UserNumbers(userID_id=user, value=number)
    db_number.save()
    db_user_number.save()
    return number


def quicksort(table, left, right):
    i = left
    j = right
    center = table[int((left + right) / 2)]
    temp = 0
    while i <= j:
        while center > table[i]:
            i = i + 1
        while center < table[j]:
            j = j - 1
        if i <= j:
            temp = table[i]
            table[i] = table[j]
            table[j] = temp
            i = i + 1
            j = j - 1

    if left < j:
        quicksort(table, left, j)

    if i < right:
        quicksort(table, i, right)

    return table


def quicksort_multi(table, left, right, elem):
    print("{0} - thread {1} is sorting {2}".format(elem, threading.current_thread(), table[left:right]))
    global przebieg
    przebieg += "{0} thread {1} is sorting {2}".format(elem, threading.current_thread(), table[left:right]) + "\n"
    elem += 1
    i = left
    j = right
    center = table[int((left + right) / 2)]
    temp = 0
    while i <= j:
        while center > table[i]:
            i = i + 1
        while center < table[j]:
            j = j - 1
        if i <= j:
            temp = table[i]
            table[i] = table[j]
            table[j] = temp
            i = i + 1
            j = j - 1

    lthread = None
    rthread = None

    if left < j:
        lthread = threading.Thread(target=lambda: quicksort_multi(table, left, j, elem))
        lthread.start()

    if i < right:
        rthread = threading.Thread(target=lambda: quicksort_multi(table, i, right, elem))
        rthread.start()

    if lthread is not None:
        lthread.join()
        del lthread
    if rthread is not None:
        rthread.join()
        del rthread

    return table
