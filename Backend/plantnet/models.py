from django.db import models

# Create your models here.
class Plant(models.Model):
    scientific_name = models.CharField(max_length=500, unique=True, primary_key=True)
    description=models.TextField()
    common_name = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='plant_photos/', )

    levels = (
        (1, 'Easy'),
        (2,'Mid'),
        (3, 'Hard'),
    )

    dificulty=models.IntegerField(
        choices=levels,
        default=1,
    )

    def __str__(self):
        return self.scientific_name