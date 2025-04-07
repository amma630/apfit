from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .utils.ai_recommendation import generate_workout_ai_recommendation
from calendar import month_name
from datetime import datetime

def generate_diet_plan_by_activity(workouts):
    activity_summary = {
        'Cardio': 0,
        'Strength': 0,
        'Yoga': 0,
        'Flexibility': 0,
        'Other': 0
    }

    for workout in workouts:
        wtype = (workout.workout_type or '').lower()
        duration = workout.duration or 0

        if 'cardio' in wtype:
            activity_summary['Cardio'] += duration
        elif 'strength' in wtype or 'weight' in wtype:
            activity_summary['Strength'] += duration
        elif 'yoga' in wtype:
            activity_summary['Yoga'] += duration
        elif 'flex' in wtype or 'stretch' in wtype:
            activity_summary['Flexibility'] += duration
        else:
            activity_summary['Other'] += duration

    plan = []
    summary = []

    if activity_summary['Cardio'] > 0:
        plan.append("🥗 High-carb meals (Oats, Fruits, Energy bars)")
        summary.append("Cardio requires quick energy — focus on good carbs.")

    if activity_summary['Strength'] > 0:
        plan.append("🍗 Protein-rich meals (Chicken, Eggs, Protein shakes)")
        summary.append("Strength training needs protein for muscle repair.")

    if activity_summary['Yoga'] > 0 or activity_summary['Flexibility'] > 0:
        plan.append("🍵 Light meals (Soups, Smoothies, Leafy greens)")
        summary.append("Light meals help with yoga & flexibility routines.")

    if not plan:
        plan.append("🍽️ Balanced diet (Fruits, Vegetables, Whole Grains)")
        summary.append("No specific activity — maintain a balanced diet.")

    return {
        'meals': plan,
        'summary': " ".join(summary),
        'activity_summary': activity_summary
    }


@login_required
def workout_list(request):
    all_workouts = Workout.objects.filter(user=request.user)  # All workouts for diet analysis
    workouts = all_workouts.order_by('-date')  # default

    selected_month = request.GET.get('month')
    if selected_month:
        workouts = workouts.filter(date__month=selected_month)

    form = WorkoutForm()
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('workout_list')

    usda_food_data = [
        {'calories': 300, 'protein': 20},
        {'calories': 250, 'protein': 15},
    ]

    ai_recommendation = generate_workout_ai_recommendation(workouts, usda_food_data)
    diet_plan = generate_diet_plan_by_activity(all_workouts)  # Use all workouts here
    total_duration = workouts.aggregate(Sum('duration'))['duration__sum'] or 0

    return render(request, 'workouts/workout_list.html', {
        'form': form,
        'workouts': workouts,
        'selected_month': selected_month,
        'months': list(enumerate(month_name))[1:],
        'total_duration': total_duration,
        'ai_recommendation': ai_recommendation,
        'diet_plan': diet_plan
    })
