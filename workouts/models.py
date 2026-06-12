from django.db import models


class Exercise(models.Model):
    """The global dictionary of available movements."""
    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.CharField(max_length=50)  # e.g., Chest, Back, Legs
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    """The overarching program container (e.g., 'Hypertrophy 4-Day Split')."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    # days => WorkoutDay List

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    """Represents a specific Day within a workout (e.g., 'Day 1: Push')."""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='days', default=None)
    name = models.CharField(max_length=100)  # e.g., "Chest & Triceps"
    order = models.PositiveIntegerField(default=0)  # Controls chronological display order

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.workout.name} - {self.name}"


class WorkoutDayRow(models.Model):
    """An individual exercise entry assigned to a specific workout day."""
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='rows', default=None)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=0)
    reps = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rest = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return f"{self.exercise.name} in {self.workout_day.name}"