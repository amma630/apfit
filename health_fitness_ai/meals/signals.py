# meals/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MealLog
from notifications.models import Notification

@receiver(post_save, sender=MealLog)
def meallog_post_save(sender, instance, created, **kwargs):
    if created:
        # Meal added
        Notification.objects.create(
            user=instance.user,
            message=f"🍽️ You added a new meal: {instance.food_name} with {instance.total_calories} kcal"
        )
    else:
        # Meal updated
        Notification.objects.create(
            user=instance.user,
            message=f"🔥 Calories updated for: {instance.food_name} → {instance.total_calories} kcal"
        )
