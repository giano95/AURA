from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_routine_remove_workoutitem_workout_day_and_more'),
    ]

    operations = [
        # Step 1: Rename old Workout -> WorkoutDay (frees up 'workouts_workout' table name)
        migrations.RenameModel(
            old_name='Workout',
            new_name='WorkoutDay',
        ),
        # Step 2: Rename Routine -> Workout (now 'workouts_workout' table name is available)
        migrations.RenameModel(
            old_name='Routine',
            new_name='Workout',
        ),
        # Step 3: Rename WorkoutItem -> WorkoutDayRow
        migrations.RenameModel(
            old_name='WorkoutItem',
            new_name='WorkoutDayRow',
        ),
        # Step 4: Rename the FK field on WorkoutDay from 'routine' -> 'workout'
        migrations.RenameField(
            model_name='workoutday',
            old_name='routine',
            new_name='workout',
        ),
        # Step 5: Rename the FK field on WorkoutDayRow from 'workout' -> 'workout_day'
        migrations.RenameField(
            model_name='workoutdayrow',
            old_name='workout',
            new_name='workout_day',
        ),
        # Step 6: Update the related_name on WorkoutDayRow from 'items' -> 'rows'
        migrations.AlterField(
            model_name='workoutdayrow',
            name='workout_day',
            field=models.ForeignKey(
                default=None,
                on_delete=models.deletion.CASCADE,
                related_name='rows',
                to='workouts.WorkoutDay',
            ),
        ),
        # Step 7: Update the related_name on WorkoutDay (stays as 'days', but points to Workout now)
        migrations.AlterField(
            model_name='workoutday',
            name='workout',
            field=models.ForeignKey(
                default=None,
                on_delete=models.deletion.CASCADE,
                related_name='days',
                to='workouts.Workout',
            ),
        ),
    ]