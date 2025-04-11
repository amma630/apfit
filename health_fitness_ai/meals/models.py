from django.db import models
from django.contrib.auth.models import User
from datetime import time

class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    quantity = models.FloatField(default=1.0)
    unit = models.CharField(max_length=20, default='grams')  # example default unit
    time = models.TimeField(default=time(8, 0))  # default to 08:00 AM
    image = models.ImageField(upload_to='meal_images/', blank=True, null=True)
    total_calories = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.quantity} {self.unit}"
