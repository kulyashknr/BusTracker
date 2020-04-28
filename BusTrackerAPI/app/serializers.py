from rest_framework import serializers
from .models import Route, Bus
from .dist import bus_info


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

    #route = RouteSerializer(many=False)










