from django.db import models


class City(models.Model):
    """
    Store openweathermap cities data
    """
    code = models.PositiveIntegerField(
        "Code"
    )
    name = models.CharField(
        "Name",
        max_length=200
    )
    state = models.CharField(
        "State",
        max_length=200,
        null=True,
        blank=True
    )
    country = models.CharField(
        "Country",
        max_length=2
    )
    lat = models.CharField(
        "Latitude",
        max_length=30
    )
    lon = models.CharField(
        "Longitude",
        max_length=30
    )

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["country", "name"]
        unique_together = ["name", "state", "country"]
