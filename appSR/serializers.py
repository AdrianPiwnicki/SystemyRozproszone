from rest_framework import serializers
from appSR.models import Numbers


class NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numbers
        fields = ['value']