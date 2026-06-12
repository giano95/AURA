from typing import List, Optional
from datetime import datetime
from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from .models import Exercise, Workout, WorkoutDay, WorkoutDayRow


# ──────────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────────

class ExerciseIn(Schema):
    name: str
    muscle_group: str
    image_url: Optional[str] = None


class ExerciseOut(Schema):
    id: int
    name: str
    muscle_group: str
    image_url: Optional[str]


class WorkoutIn(Schema):
    name: str


class WorkoutOut(Schema):
    id: int
    name: str
    created_at: str  # ISO 8601 string

    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.isoformat() if obj.created_at else ""


class WorkoutDayIn(Schema):
    name: str
    order: int = 0


class WorkoutDayPatchIn(Schema):
    name: Optional[str] = None
    order: Optional[int] = None


class WorkoutDayOut(Schema):
    id: int
    workout_id: int
    name: str
    order: int


class WorkoutDayRowIn(Schema):
    exercise_id: int
    sets: int = 0
    reps: int = 0
    weight: float = 0.0
    rest: str = ""


class WorkoutDayRowOut(Schema):
    id: int
    workout_day_id: int
    exercise_id: int
    exercise_name: str = ""
    sets: int
    reps: int
    weight: float
    rest: str


class WorkoutDayRowUpdateIn(Schema):
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    rest: Optional[str] = None


# ──────────────────────────────────────────────
# Router
# ──────────────────────────────────────────────

router = Router(tags=["workouts"])


# -- Exercises -----------------------------------------------------

@router.get("/exercises/", response=List[ExerciseOut])
def list_exercises(request):
    qs = Exercise.objects.all().order_by("name")
    return qs


@router.post("/exercises/", response=ExerciseOut)
def create_exercise(request, payload: ExerciseIn):
    exercise = Exercise.objects.create(
        name=payload.name,
        muscle_group=payload.muscle_group,
        image_url=payload.image_url,
    )
    return exercise


@router.get("/exercises/{exercise_id}/", response=ExerciseOut)
def get_exercise(request, exercise_id: int):
    return get_object_or_404(Exercise, id=exercise_id)


@router.put("/exercises/{exercise_id}/", response=ExerciseOut)
def update_exercise(request, exercise_id: int, payload: ExerciseIn):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    for attr, value in payload.dict().items():
        setattr(exercise, attr, value)
    exercise.save()
    return exercise


@router.delete("/exercises/{exercise_id}/", response={204: None})
def delete_exercise(request, exercise_id: int):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    exercise.delete()
    return 204, None


# -- Workouts ------------------------------------------------------

@router.get("/workouts/", response=List[WorkoutOut])
def list_workouts(request):
    qs = Workout.objects.all().order_by("-created_at")
    return qs


@router.post("/workouts/", response=WorkoutOut)
def create_workout(request, payload: WorkoutIn):
    workout = Workout.objects.create(name=payload.name)
    return workout


@router.get("/workouts/{workout_id}/", response=WorkoutOut)
def get_workout(request, workout_id: int):
    return get_object_or_404(Workout, id=workout_id)


@router.put("/workouts/{workout_id}/", response=WorkoutOut)
def update_workout(request, workout_id: int, payload: WorkoutIn):
    workout = get_object_or_404(Workout, id=workout_id)
    workout.name = payload.name
    workout.save()
    return workout


@router.delete("/workouts/{workout_id}/", response={204: None})
def delete_workout(request, workout_id: int):
    workout = get_object_or_404(Workout, id=workout_id)
    workout.delete()
    return 204, None


# -- WorkoutDays (Days within a Workout) ---------------------------

@router.get("/workouts/{workout_id}/days/", response=List[WorkoutDayOut])
def list_workout_days(request, workout_id: int):
    workout = get_object_or_404(Workout, id=workout_id)
    return workout.days.all()


@router.post("/workouts/{workout_id}/days/", response=WorkoutDayOut)
def create_workout_day(request, workout_id: int, payload: WorkoutDayIn):
    workout = get_object_or_404(Workout, id=workout_id)
    workout_day = WorkoutDay.objects.create(
        workout=workout,
        name=payload.name,
        order=payload.order,
    )
    return workout_day


@router.get("/workout-days/{workout_day_id}/", response=WorkoutDayOut)
def get_workout_day(request, workout_day_id: int):
    return get_object_or_404(WorkoutDay, id=workout_day_id)


@router.put("/workout-days/{workout_day_id}/", response=WorkoutDayOut)
def update_workout_day(request, workout_day_id: int, payload: WorkoutDayPatchIn):
    workout_day = get_object_or_404(WorkoutDay, id=workout_day_id)
    data = payload.dict(exclude_unset=True)
    for attr, value in data.items():
        setattr(workout_day, attr, value)
    workout_day.save()
    return workout_day


@router.delete("/workout-days/{workout_day_id}/", response={204: None})
def delete_workout_day(request, workout_day_id: int):
    workout_day = get_object_or_404(WorkoutDay, id=workout_day_id)
    workout_day.delete()
    return 204, None


# -- WorkoutDayRows (Exercises inside a WorkoutDay) ----------------

@router.get("/workout-days/{workout_day_id}/rows/", response=List[WorkoutDayRowOut])
def list_rows(request, workout_day_id: int):
    workout_day = get_object_or_404(WorkoutDay, id=workout_day_id)
    return [
        {
            "id": row.id,
            "workout_day_id": row.workout_day_id,
            "exercise_id": row.exercise_id,
            "exercise_name": row.exercise.name,
            "sets": row.sets,
            "reps": row.reps,
            "weight": row.weight,
            "rest": row.rest,
        }
        for row in workout_day.rows.all()
    ]


@router.post("/workout-days/{workout_day_id}/rows/", response=WorkoutDayRowOut)
def create_row(request, workout_day_id: int, payload: WorkoutDayRowIn):
    workout_day = get_object_or_404(WorkoutDay, id=workout_day_id)
    exercise = get_object_or_404(Exercise, id=payload.exercise_id)
    row = WorkoutDayRow.objects.create(
        workout_day=workout_day,
        exercise=exercise,
        sets=payload.sets,
        reps=payload.reps,
        weight=payload.weight,
        rest=payload.rest,
    )
    return {
        "id": row.id,
        "workout_day_id": row.workout_day_id,
        "exercise_id": row.exercise_id,
        "exercise_name": row.exercise.name,
        "sets": row.sets,
        "reps": row.reps,
        "weight": row.weight,
        "rest": row.rest,
    }


@router.put("/rows/{row_id}/", response=WorkoutDayRowOut)
def update_row(request, row_id: int, payload: WorkoutDayRowUpdateIn):
    row = get_object_or_404(WorkoutDayRow, id=row_id)
    update_data = payload.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(row, attr, value)
    row.save()
    return {
        "id": row.id,
        "workout_day_id": row.workout_day_id,
        "exercise_id": row.exercise_id,
        "exercise_name": row.exercise.name,
        "sets": row.sets,
        "reps": row.reps,
        "weight": row.weight,
        "rest": row.rest,
    }


@router.delete("/rows/{row_id}/", response={204: None})
def delete_row(request, row_id: int):
    row = get_object_or_404(WorkoutDayRow, id=row_id)
    row.delete()
    return 204, None