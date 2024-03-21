from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class GroupedFlightsSerializer(serializers.Serializer):
    def __init__(self, main: QuerySet, others: QuerySet, **args):
        super().__init__(**args)
        self.main = serializers.ListSerializer(child=FlightSerializer(main))
        self.others = serializers.ListSerializer(child=FlightSerializer(others))
