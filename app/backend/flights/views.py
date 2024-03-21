from rest_framework import viewsets
from django.db.models.query import QuerySet

from .models import Flight
from .serializers import FlightSerializer


# Create your views here.
class FlightsViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        query_set: QuerySet = super().get_queryset()

        destination = self.request.GET.get("city")
        date = self.request.GET.get("date") # TODO: Use date to validate

        if destination is not None and date is not None:
            query_set = query_set.filter(city_destination=destination)

        return query_set
