from datetime import timedelta
from django.db.models import Min
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Flight
from .serializers import FlightSerializer, GroupedFlightsSerializer


# Create your views here.
class FlightsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flight.objects.all()

    MAIN_FLIGHT_MAX_COUNT = 2

    def list(self, request, *args, **kwargs):
        super().list(self)
        # Copied from super().list() implementation
        queryset: QuerySet = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        cheap_flights: float = queryset.filter(
            price_comfort=queryset.aggregate(Min("price_economic"))
        )
        faster_flights: timedelta = queryset.filter(
            duration=queryset.aggregate(Min("duration"))
        )

        others = queryset.exclude(cheap_flights).exclude(faster_flights)

        serializer = GroupedFlightsSerializer(
            data={
                "main": cheap_flights + faster_flights,
                "others": others,
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    def get_queryset(self):
        query_set: QuerySet = super().get_queryset()

        destination = self.request.GET.get("city")
        date = self.request.GET.get("date")  # TODO: Use date to validate

        if destination is not None and date is not None:
            query_set = query_set.filter(city_destination=destination)

        return query_set
