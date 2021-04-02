from django.urls import include, path
from rest_framework import routers
from appSR import views

router = routers.DefaultRouter()
router.register(r'getNumbers', views.NumbersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

