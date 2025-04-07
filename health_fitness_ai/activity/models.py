from django.db import models
from django.contrib.auth.models import User

class Activity(models.Model):
    ACTIVITY_CHOICES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('gym', 'Gym Workout'),
        ('yoga', 'Yoga'),
        ('swimming', 'Swimming')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    duration = models.IntegerField(help_text='Duration in minutes')
    gaps = models.IntegerField(default=0, help_text='Rest time in seconds')
    calories_burned = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.calories_burned = self.calculate_calories()
        super().save(*args, **kwargs)
    
    def calculate_calories(self):
        MET_VALUES = {
            'running': 9.8,
            'walking': 3.8,
            'cycling': 7.5,
            'gym': 6.0,
            'yoga': 2.5,
            'swimming': 8.0,
        }
        user_weight = self.user.userprofile.weight if hasattr(self.user, 'userprofile') else 70  # Default 70kg
        met = MET_VALUES.get(self.activity_name, 5.0)
        return (met * user_weight * self.duration) / 60
