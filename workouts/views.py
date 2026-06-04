from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from .models import Routine, Workout, WorkoutItem, Exercise


def routine_dashboard(request, routine_id):
    """Initial base layout renderer loading the core interface shell."""
    routine = get_object_or_404(Routine, id=routine_id)

    # Check if days exist. If not, auto-create Day 1 to avoid an empty application state
    workout = routine.days.first()
    if not workout:
        workout = Workout.objects.create(
            routine=routine,
            name="Day 1: New Workout",
            order=1
        )

    exercises = Exercise.objects.all()[:15]  # Populate initial search pool

    return render(request, 'workouts/workout_edit.html', {
        'routine': routine,
        'workout': workout,
        'exercises': exercises
    })


@require_http_methods(["POST"])
def create_workout_day(request, routine_id):
    """Generates a new sequential workout day tab and automatically sets it as active."""
    routine = get_object_or_404(Routine, id=routine_id)

    # Calculate the next order sequence number
    next_order = routine.days.count() + 1

    # Instantiate the new day with a generic placeholder title
    new_workout = Workout.objects.create(
        routine=routine,
        name=f"Day {next_order}",
        order=next_order
    )

    # Grab initial exercise pool for the right sidebar layout panel
    exercises = Exercise.objects.all()[:15]

    # Return the entire updated workspace with the new day open
    return render(request, 'workouts/workout_edit.html', {
        'routine': routine,
        'workout': new_workout,
        'exercises': exercises
    })


def get_workout_day(request, workout_id):
    """Swaps the active training day view completely when a tab is clicked."""
    workout = get_object_or_404(Workout, id=workout_id)
    routine = workout.routine
    exercises = Exercise.objects.all()[:15]

    # Re-renders the core grid component using updated context fields
    return render(request, 'workouts/workout_edit.html', {
        'routine': routine,
        'workout': workout,
        'exercises': exercises
    })


@require_http_methods(["POST"])
def update_workout_name(request, workout_id):
    """Saves real-time title edits directly from the top heading element."""
    workout = get_object_or_404(Workout, id=workout_id)
    workout.name = request.POST.get('workout_name', workout.name)
    workout.save()
    return HttpResponse(workout.name)


@require_http_methods(["POST"])
def update_exercise_row(request, item_id):
    """Processes instant inline database modifications as input metrics shift."""
    item = get_object_or_404(WorkoutItem, id=item_id)
    item.sets = int(request.POST.get('sets', 0))
    item.reps = int(request.POST.get('reps', 0))
    item.weight = float(request.POST.get('weight', 0.0))
    item.rest = request.POST.get('rest', '')
    item.save()

    # Returns only the updated row snippet using native Django 6 partial targets
    return render(request, 'workouts/workout_edit.html#workout_row', {'item': item})


@require_http_methods(["DELETE"])
def delete_exercise_row(request, item_id):
    """Removes a row database entry and outputs an empty response to clear the element."""
    item = get_object_or_404(WorkoutItem, id=item_id)
    item.delete()
    return HttpResponse("")  # HTMX deletes target element cleanly when receiving 200 OK blank responses


def search_exercises(request, workout_id):
    """Filters data matching partial strings typed into the search menu."""
    query = request.GET.get('search', '').strip()
    if query:
        exercises = Exercise.objects.filter(name__icontains=query)
    else:
        exercises = Exercise.objects.all()[:15]

    return render(request, 'workouts/workout_edit.html#exercise_pool', {
        'exercises': exercises,
        'workout': get_object_or_404(Workout, id=workout_id)
    })


@require_http_methods(["POST"])
def add_exercise_row(request, workout_id):
    """Appends an existing reference exercise to the active workout grid."""
    workout = get_object_or_404(Workout, id=workout_id)
    exercise_id = request.POST.get('exercise_id')
    exercise = get_object_or_404(Exercise, id=exercise_id)

    item = WorkoutItem.objects.create(workout=workout, exercise=exercise)
    return render(request, 'workouts/workout_edit.html#workout_row', {'item': item})


@require_http_methods(["POST"])
def create_and_add_exercise(request, workout_id):
    """Creates a completely custom exercise entry and assigns it instantly."""
    workout = get_object_or_404(Workout, id=workout_id)
    name = request.POST.get('name')
    muscle_group = request.POST.get('muscle_group')
    image_url = request.POST.get('image_url') or None

    exercise, created = Exercise.objects.get_or_create(
        name=name,
        defaults={'muscle_group': muscle_group, 'image_url': image_url}
    )

    item = WorkoutItem.objects.create(workout=workout, exercise=exercise)
    return render(request, 'workouts/workout_edit.html#workout_row', {'item': item})


def get_search_tab(request, workout_id):
    """Renders the standard exercise search panel snippet via HTMX tab switches."""
    workout = get_object_or_404(Workout, id=workout_id)
    exercises = Exercise.objects.all()[:15]
    return render(request, 'workouts/workout_edit.html#search_tab', {'workout': workout, 'exercises': exercises})


def get_create_tab(request, workout_id):
    """Renders the clean exercise creation layout form view."""
    workout = get_object_or_404(Workout, id=workout_id)
    return render(request, 'workouts/workout_edit.html#create_tab', {'workout': workout})