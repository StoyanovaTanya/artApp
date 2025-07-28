from django.contrib.auth import get_user_model
from django.db import models
from artwork.models import Artwork

UserModel = get_user_model()

class Event(models.Model):
    title = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        max_length=300,
    )

    location = models.CharField(
        max_length=100,
    )

    date = models.DateTimeField()

    image = models.ImageField(
        upload_to='event_images/',
        null=True,
        blank=True,
    )

    artworks = models.ManyToManyField(
        Artwork,
        related_name='events',
    )

    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='created_events',
    )

    def __str__(self):
        return f"{self.title} on {self.date.date()}"
