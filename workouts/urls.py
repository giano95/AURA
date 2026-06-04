from django.urls import path
from . import views

urlpatterns = [
    # Main Dashboard Initial Page Load
    path('routine/<int:routine_id>/', views.routine_dashboard, name='routine_dashboard'),
    path('routine/<int:routine_id>/days/create/', views.create_workout_day, name='create_workout_day'),

    # Day-to-Day Navigation Switching Engine
    path('workout/<int:workout_id>/get/', views.get_workout_day, name='get_workout_day'),
    path('workout/<int:workout_id>/update-name/', views.update_workout_name, name='update_workout_name'),

    # Exercise Item Inline Calculations & Row Operations
    path('item/<int:item_id>/update/', views.update_exercise_row, name='update_exercise_row'),
    path('item/<int:item_id>/delete/', views.delete_exercise_row, name='delete_exercise_row'),

    # Sidebar Tab & Searching Components
    path('workout/<int:workout_id>/tabs/search/', views.get_search_tab, name='get_search_tab'),
    path('workout/<int:workout_id>/tabs/create/', views.get_create_tab, name='get_create_tab'),
    path('workout/<int:workout_id>/exercises/search/', views.search_exercises, name='search_exercises'),

    # Insertion / Creation Endpoints
    path('workout/<int:workout_id>/exercises/add/', views.add_exercise_row, name='add_exercise_row'),
    path('workout/<int:workout_id>/exercises/create-custom/', views.create_and_add_exercise,
         name='create_and_add_exercise'),
]