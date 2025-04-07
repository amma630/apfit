from django.db import models
from django.contrib.auth.models import User

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    date = models.DateField()

    def __str__(self):
        return f"{self.workout_type} - {self.duration} min"
