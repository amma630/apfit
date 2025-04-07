# workouts/admin.py
from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_type', 'duration', 'date')
    list_filter = ('workout_type', 'date')
    search_fields = ('user__username', 'workout_type')
