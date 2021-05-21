from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from appSR import views

router = DefaultRouter()
router.register('numbers', views.NumbersViewSet)

urlpatterns = [
    path('getNumbers/', views.list_number),
    path('login/', views.log_user),
    path('postNumbers/', views.generate_numbers),
    path('bubbleSort/', views.bubble_sort),
    path('multithreadingQuickSort/', views.quick_sort_multithreading),
    path('quickSort/', views.quick_sort_notthreading),
    path('', include(router.urls)),
]
