# from django.db import models
#
#
# class Workout(models.Model):
#     """The master program (e.g., 'Hypertrophy 4-Day Split', 'Summer Shred')"""
#     name = models.CharField(max_length=100)
#     created_at = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#
# class WorkoutDay(models.Model):
#     """The specific day within that routine (e.g., 'Day 1: Chest & Tri', 'Leg Day')"""
#     routine = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='days')
#     name = models.CharField(max_length=100)  # e.g., "Pull Day", "Back & Biceps"
#     order = models.PositiveIntegerField(default=1)  # To keep Day 1, Day 2, Day 3 in sequence
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return f"{self.routine.name} - {self.name}"
#
#
# class Exercise(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     muscle_group = models.CharField(max_length=50, default="None", help_text="e.g., Biceps, Chest, Shoulders")
#     image_url = models.URLField(blank=True, null=True, help_text="URL to exercise thumbnail")
#
#     def __str__(self):
#         return self.name
#
#
# class WorkoutItem(models.Model):
#     """The actual exercises assigned to that specific day"""
#     workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE, related_name='items')
#     exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
#     sets = models.PositiveIntegerField(default=3)
#     reps = models.PositiveIntegerField(default=10)
#     weight = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
#     rest = models.CharField(max_length=20, default="60s")

from django.db import models


class Exercise(models.Model):
    """The global dictionary of available movements."""
    name = models.CharField(max_length=100, unique=True)
    muscle_group = models.CharField(max_length=50)  # e.g., Chest, Back, Legs
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Routine(models.Model):
    """The overarching program container (e.g., 'Hypertrophy 4-Day Split')."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    """Represents a specific Day within a routine (e.g., 'Day 1: Push')."""
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name='days', default=None)
    name = models.CharField(max_length=100)  # e.g., "Chest & Triceps"
    order = models.PositiveIntegerField(default=0)  # Controls chronological display order

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.routine.name} - {self.name}"


class WorkoutItem(models.Model):
    """An individual exercise entry assigned to a specific workout day."""
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='items', default=None)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=0)
    reps = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rest = models.CharField(max_length=20, blank=True, default="")

    def __str__(self):
        return f"{self.exercise.name} in {self.workout.name}"
