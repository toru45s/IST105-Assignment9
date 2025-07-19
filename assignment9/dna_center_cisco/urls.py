from django.urls import path
from .views import unified_dashboard

urlpatterns = [
    path("", unified_dashboard, name="dashboard"),
]