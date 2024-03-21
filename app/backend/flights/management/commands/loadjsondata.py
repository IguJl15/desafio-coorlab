from datetime import timedelta
from decimal import Decimal
import json
from django.core.management.base import BaseCommand
from pytimeparse import timeparse
from flights.models import Flight


class Command(BaseCommand):
    help = "Load the data.json provided"
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument("input", type=str)

    def handle(self, *args, **options):
        with open(options["input"]) as file:
            data = json.load(file)
            flights: list[dict] = data["transport"]

            for flight_json in flights:
                price_comfort = self.parse_price(flight_json["price_confort"])
                price_economic = self.parse_price(flight_json["price_econ"])

                duration_seconds = timeparse.timeparse(flight_json["duration"])
                duration = timedelta(seconds=duration_seconds)

                Flight.objects.create(
                    company_name=flight_json["name"],
                    city_destination=flight_json["city"],
                    comfort_bed_location=flight_json["bed"],
                    economic_seat_location=flight_json["seat"],
                    duration=duration,
                    price_comfort=price_comfort,
                    price_economic=price_economic,
                    city_from="Teresina",
                )
            self.stdout.write(
                "JSON loaded to the database successfully! %s items added"
                % len(flights)
            )

    def parse_price(self, value: str):
        return Decimal(value.strip("R$ "))
