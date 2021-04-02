from django.urls import include, path
from rest_framework.routers import DefaultRouter

from appSR import views

router = DefaultRouter()
router.register('numbers', views.NumbersViewSet)

urlpatterns = [
    path('getNumbers/', views.list_number),
    path('postNumbers/', views.generate_numbers),
    path('', include(router.urls)),
]
