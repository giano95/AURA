from rest_framework import serializers
from models import *


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_name = serializers.CharField(
        source="exercise.name",
        read_only=True
    )

    class Meta:
        model = WorkoutExercise
        fields = [
            "id",
            "exercise",
            "exercise_name",
            "order",
            "sets",
            "notes",
        ]


class WorkoutSerializer(serializers.ModelSerializer):
    rows = WorkoutExerciseSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Workout
        fields = [
            "id",
            "name",
            "rows",
        ]
