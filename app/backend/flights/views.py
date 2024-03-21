from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Flight
from .serializers import FlightSerializer, GroupedFlightsSerializer


# Create your views here.
class FlightsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    MAIN_FLIGHT_MAX_COUNT = 2

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data

        main_flights = data[: self.MAIN_FLIGHT_MAX_COUNT]
        other_flights = data[self.MAIN_FLIGHT_MAX_COUNT :]

        serializer = GroupedFlightsSerializer(
            data={
                "main": main_flights,
                "others": other_flights,
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
