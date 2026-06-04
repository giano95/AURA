from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from aura import views
from workouts.api import router as workouts_router

api = NinjaAPI(
    title="AURA API",
    version="1.0.0",
    description="Fitness coaching platform API — powers the web app and mobile clients.",
)

api.add_router("/workouts/", workouts_router, tags=["workouts"])

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('coach/', include('coach.urls')),
    path('', include('workouts.urls')),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
