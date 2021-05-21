from rest_framework import serializers
from appSR.models import Numbers, UserSystem


class NumbersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Numbers
        fields = ['value']


class UserSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSystem
        fields = ['name', 'hash']
