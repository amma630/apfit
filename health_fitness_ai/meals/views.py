import json
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import MealLog
from .forms import MealLogForm
from .utils import get_usda_nutrition
from notifications.models import Notification

CALORIE_MIN = 1200
CALORIE_MAX = 2200

# Calculate daily totals
def get_day_totals(user, day):
    logs = MealLog.objects.filter(user=user, date=day)
    return {
        'logs': logs,
        'calories': sum((log.total_calories or 0) for log in logs),
        'protein': sum((log.protein or 0) for log in logs),
        'carbs': sum((log.carbs or 0) for log in logs),
        'fat': sum((log.fat or 0) for log in logs),
    }

# Meal Log View
@login_required
def meal_log_view(request):
    today = date.today()
    if request.method == 'POST':
        form = MealLogForm(request.POST, request.FILES)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user

            food_name = form.cleaned_data.get('food_name')
            quantity = form.cleaned_data.get('quantity') or 1
            unit = form.cleaned_data.get('unit')

            if not food_name:
                messages.error(request, "Please select a food item.")
                return redirect('meal_log')

            meal.food_name = food_name
            meal.quantity = quantity
            meal.unit = unit

            # Fetch USDA nutrition
            nutrition = get_usda_nutrition(food_name, quantity, unit)
            if nutrition:
                meal.total_calories = nutrition['calories']
                meal.protein = nutrition['protein']
                meal.carbs = nutrition['carbs']
                meal.fat = nutrition['fat']
            else:
                messages.warning(request, f"No nutrition data found for {food_name}.")

            meal.save()

            # Notification
            Notification.objects.create(
                user=request.user,
                message=f"You logged {meal.food_name} with {meal.total_calories} kcal."
            )

            # Email
            try:
                send_mail(
                    subject='🍽️ Meal Logged!',
                    message=f"Hi {request.user.username},\n\nYou logged {meal.food_name} ({quantity} {unit}) with {meal.total_calories} kcal!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[request.user.email],
                    fail_silently=True
                )
            except Exception as e:
                print(f"Email error: {e}")

            return redirect('meal_log')
    else:
        form = MealLogForm()

    # Today totals
    today_totals = get_day_totals(request.user, today)

    # Recommendation
    if today_totals['calories'] < CALORIE_MIN:
        recommendation = "Eat a bit more — maybe something rich in protein 🍗"
    elif today_totals['calories'] > CALORIE_MAX:
        recommendation = "You've eaten a lot — try something light 🥗"
    else:
        recommendation = "You're doing great! 🎉"

    # Weekly overview
    week_dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    weekly_data = []
    weekly_labels = []
    weekly_calories = []

    for day in week_dates:
        totals = get_day_totals(request.user, day)
        weekly_data.append({'date': day.strftime('%a'), **totals})
        weekly_labels.append(day.strftime('%a'))
        weekly_calories.append(totals['calories'])

    # Macros for today
    today_macros = {
        'protein': today_totals['protein'],
        'carbs': today_totals['carbs'],
        'fat': today_totals['fat'],
    }
    total_macros = sum(today_macros.values()) or 1
    macro_percentages = {k: round((v / total_macros) * 100) for k, v in today_macros.items()}
    most_eaten_macro = max(macro_percentages, key=macro_percentages.get)
    least_eaten_macro = min(macro_percentages, key=macro_percentages.get)

    return render(request, 'meals/meal_log.html', {
        'form': form,
        'logs': today_totals['logs'],
        'total_calories': today_totals['calories'],
        'recommendation': recommendation,
        'weekly_data': weekly_data,
        'weekly_labels': json.dumps(weekly_labels),
        'weekly_calories': json.dumps(weekly_calories),
        'macro_percentages': macro_percentages,
        'most_eaten_macro': most_eaten_macro,
        'least_eaten_macro': least_eaten_macro,
        'most_percentage': macro_percentages[most_eaten_macro],
        'least_percentage': macro_percentages[least_eaten_macro],
    })

# Dashboard View
from django.shortcuts import render
from .models import MealLog
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    meals = MealLog.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'dashboard.html', {'meals': meals})
