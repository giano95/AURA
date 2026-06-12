from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from coach.decorators import coach_required
from workouts.models import Workout


@login_required
@coach_required
def coach_home(request):
    return render(request, 'coach/home.html', {})


@login_required
@coach_required
def coach_clients(request):
    return render(request, 'coach/clients.html', {})


@login_required
@coach_required
def coach_documents(request):
    workouts = Workout.objects.all().order_by('-created_at')
    return render(request, 'coach/documents.html', {'workouts': workouts})


@login_required
@coach_required
def coach_dashboard(request):
    return render(request, 'coach/dashboard.html', {})


@login_required
@coach_required
def coach_messages(request):
    return render(request, 'coach/messages.html', {})