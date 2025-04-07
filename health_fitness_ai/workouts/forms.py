from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):  # ✅ Correct
    class Meta:
        model = Workout
        fields = ['workout_type', 'duration', 'date']



