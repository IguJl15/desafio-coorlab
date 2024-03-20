from django.db import models


# Create your models here.
class Flight(models.Model):
    company_name = models.CharField("Company Name", max_length=300)
    price_comfort = models.DecimalField(
        "Price Comfort", max_digits=10, decimal_places=2
    )
    price_economic = models.DecimalField(
        "Price Economic", max_digits=10, decimal_places=2
    )
    city_from = models.CharField("From City", max_length=300)
    city_destination = models.CharField("To City", max_length=300)
    duration = models.DurationField("Duration")
    comfort_bed_location = models.CharField("Comfort Bed Location", max_length=50)
    economic_seat_location = models.CharField("Economic Seat Location", max_length=50)

    class Meta:
        verbose_name = "Flight"
        verbose_name_plural = "Flights"

    def __str__(self):
        return self.company_name
