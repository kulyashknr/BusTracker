from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .models import Route, Bus
from .serializers import RouteSerializer, BusSerializer
from .dist import *


class RouteView(APIView):
    http_method_names = ['post']
    lookup_field = 'id'

    def post(self, request):
        Bus.objects.all().delete()
        Route.objects.all().delete()

        serializer = RouteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            first = serializer.data['start_station']
            second = serializer.data['end_station']

            get_buses(first, second)

            # for station in jsonData:
            #     if (first.lower() in station["Nm"].lower()):
            #         station_lt = station["Pt"]["Y"]
            #         station_ln = station["Pt"]["X"]


            for i in range(0, len(bus_info)):
                # get_route(bus_info[i][0])
                # bus_lt, bus_ln = bus_info[i][1]
                # dist = route_dir(station_lt, station_ln, bus_lt, bus_ln)
                Bus.objects.create(name=bus_info[i][0], number=bus_info[i][1], distance=bus_info[i][2], route_id=serializer.data['id'])

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        bus_info.clear()
        Bus.objects.all().delete()
        Route.objects.all().delete()



class getBuses(ListAPIView):
    serializer_class = BusSerializer
    lookup_field = 'route_id'

    def get_queryset(self):
        return Bus.objects.filter(route_id=self.kwargs[self.lookup_field])