from django.db import models
from django.contrib.auth import get_user_model

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
    

User = get_user_model()

class UserChallenge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='current_challenge_record')
    current_challange=models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='current_challenge')

    #track when challange set
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s challange: {self.current_challange.scientific_name}"