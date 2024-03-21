from rest_framework import serializers
from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class GroupedFlightsSerializer(serializers.Serializer):
    main = serializers.ListSerializer(child=FlightSerializer())
    others = serializers.ListSerializer(child=FlightSerializer())
