from typing import List, Optional
from datetime import datetime
from ninja import Router, Schema
from django.shortcuts import get_object_or_404
from .models import Exercise, Routine, Workout, WorkoutItem


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


class RoutineIn(Schema):
    name: str


class RoutineOut(Schema):
    id: int
    name: str
    created_at: str  # ISO 8601 string

    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.isoformat() if obj.created_at else ""


class WorkoutIn(Schema):
    name: str
    order: int = 0


class WorkoutPatchIn(Schema):
    name: Optional[str] = None
    order: Optional[int] = None


class WorkoutOut(Schema):
    id: int
    routine_id: int
    name: str
    order: int


class WorkoutItemIn(Schema):
    exercise_id: int
    sets: int = 0
    reps: int = 0
    weight: float = 0.0
    rest: str = ""


class WorkoutItemOut(Schema):
    id: int
    workout_id: int
    exercise_id: int
    exercise_name: str = ""
    sets: int
    reps: int
    weight: float
    rest: str


class WorkoutItemUpdateIn(Schema):
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


# -- Routines ------------------------------------------------------

@router.get("/routines/", response=List[RoutineOut])
def list_routines(request):
    qs = Routine.objects.all().order_by("-created_at")
    return qs


@router.post("/routines/", response=RoutineOut)
def create_routine(request, payload: RoutineIn):
    routine = Routine.objects.create(name=payload.name)
    return routine


@router.get("/routines/{routine_id}/", response=RoutineOut)
def get_routine(request, routine_id: int):
    return get_object_or_404(Routine, id=routine_id)


@router.put("/routines/{routine_id}/", response=RoutineOut)
def update_routine(request, routine_id: int, payload: RoutineIn):
    routine = get_object_or_404(Routine, id=routine_id)
    routine.name = payload.name
    routine.save()
    return routine


@router.delete("/routines/{routine_id}/", response={204: None})
def delete_routine(request, routine_id: int):
    routine = get_object_or_404(Routine, id=routine_id)
    routine.delete()
    return 204, None


# -- Workouts (Days within a Routine) ------------------------------

@router.get("/routines/{routine_id}/workouts/", response=List[WorkoutOut])
def list_workouts(request, routine_id: int):
    routine = get_object_or_404(Routine, id=routine_id)
    return routine.days.all()


@router.post("/routines/{routine_id}/workouts/", response=WorkoutOut)
def create_workout(request, routine_id: int, payload: WorkoutIn):
    routine = get_object_or_404(Routine, id=routine_id)
    workout = Workout.objects.create(
        routine=routine,
        name=payload.name,
        order=payload.order,
    )
    return workout


@router.get("/workouts/{workout_id}/", response=WorkoutOut)
def get_workout(request, workout_id: int):
    return get_object_or_404(Workout, id=workout_id)


@router.put("/workouts/{workout_id}/", response=WorkoutOut)
def update_workout(request, workout_id: int, payload: WorkoutPatchIn):
    workout = get_object_or_404(Workout, id=workout_id)
    data = payload.dict(exclude_unset=True)
    for attr, value in data.items():
        setattr(workout, attr, value)
    workout.save()
    return workout


@router.delete("/workouts/{workout_id}/", response={204: None})
def delete_workout(request, workout_id: int):
    workout = get_object_or_404(Workout, id=workout_id)
    workout.delete()
    return 204, None


# -- Workout Items (Exercises inside a Workout) --------------------

@router.get("/workouts/{workout_id}/items/", response=List[WorkoutItemOut])
def list_items(request, workout_id: int):
    workout = get_object_or_404(Workout, id=workout_id)
    return [
        {
            "id": item.id,
            "workout_id": item.workout_id,
            "exercise_id": item.exercise_id,
            "exercise_name": item.exercise.name,
            "sets": item.sets,
            "reps": item.reps,
            "weight": item.weight,
            "rest": item.rest,
        }
        for item in workout.items.all()
    ]


@router.post("/workouts/{workout_id}/items/", response=WorkoutItemOut)
def create_item(request, workout_id: int, payload: WorkoutItemIn):
    workout = get_object_or_404(Workout, id=workout_id)
    exercise = get_object_or_404(Exercise, id=payload.exercise_id)
    item = WorkoutItem.objects.create(
        workout=workout,
        exercise=exercise,
        sets=payload.sets,
        reps=payload.reps,
        weight=payload.weight,
        rest=payload.rest,
    )
    return {
        "id": item.id,
        "workout_id": item.workout_id,
        "exercise_id": item.exercise_id,
        "exercise_name": item.exercise.name,
        "sets": item.sets,
        "reps": item.reps,
        "weight": item.weight,
        "rest": item.rest,
    }


@router.put("/items/{item_id}/", response=WorkoutItemOut)
def update_item(request, item_id: int, payload: WorkoutItemUpdateIn):
    item = get_object_or_404(WorkoutItem, id=item_id)
    update_data = payload.dict(exclude_unset=True)
    for attr, value in update_data.items():
        setattr(item, attr, value)
    item.save()
    return {
        "id": item.id,
        "workout_id": item.workout_id,
        "exercise_id": item.exercise_id,
        "exercise_name": item.exercise.name,
        "sets": item.sets,
        "reps": item.reps,
        "weight": item.weight,
        "rest": item.rest,
    }


@router.delete("/items/{item_id}/", response={204: None})
def delete_item(request, item_id: int):
    item = get_object_or_404(WorkoutItem, id=item_id)
    item.delete()
    return 204, None