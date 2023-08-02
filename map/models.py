from django.db import models

# Create your models here.


class MapPoint(models.Model):
    # Define your model fields here
    locationNumber = models.IntegerField()
    isGuess = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    # Add more fields as needed

    # Optionally, define any relationships with other models
    #related_model = models.ForeignKey('RelatedModel', on_delete=models.CASCADE)