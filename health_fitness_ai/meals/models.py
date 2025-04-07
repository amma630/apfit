from django.db import models
from django.contrib.auth.models import User

class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    total_calories = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.food_name} - {self.date}"
