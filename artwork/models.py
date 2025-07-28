from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class Artwork(models.Model):
    title = models.CharField(
        max_length=100,
    )

    artist_name = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        max_length=300,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    image = models.ImageField(
        upload_to='artwork_images/',
    )

    owner = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='artworks',
    )

    def __str__(self):
        return self.title