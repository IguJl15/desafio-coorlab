from datetime import timedelta
from django.db.models import Min
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Flight
from .serializers import FlightSerializer


# Create your views here.
class FlightsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def list(self, request, *args, **kwargs):
        # super().list()
        # Copied from super().list() implementation
        queryset: QuerySet = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            main_serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(main_serializer.data)
        # end copy

        minimums = queryset.aggregate(
            price=Min("price_economic"), duration=Min("duration")
        )

        faster_flights = queryset.filter(duration=minimums["duration"])
        # TODO: remove cheaper flights that have the price higher than the comfort option.
        # Maybe add some feedback as a promotion "We have the cheapest comfort bed for you!"
        cheap_flights = queryset.filter(price_economic=minimums["price"])

        all_selected_flights = cheap_flights.union(faster_flights)

        others = queryset.exclude(
            id__in=all_selected_flights.values_list("id", flat=True)
        )

        comfort_serializer = self.get_serializer(faster_flights, many=True)
        economic_serializer = self.get_serializer(cheap_flights, many=True)
        others_serializer = self.get_serializer(others, many=True)

        return Response(
            {
                "comfort": comfort_serializer.data,
                "economic": economic_serializer.data,
                "others": others_serializer.data,
            }
        )

    def get_queryset(self):
        query_set: QuerySet = super().get_queryset()

        destination = self.request.GET.get("city")
        date = self.request.GET.get("date")  # TODO: Use date to validate

        if destination is not None and date is not None:
            query_set = query_set.filter(city_destination=destination)

        return query_set
