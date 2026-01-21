
from django.urls import path
from . import views
urlpatterns = [
    path("dashboard", views.dashboard_view, name="dashboard"),
    path("ventures", views.venture_list, name="venture_list"),
    path("add-venture", views.save_venture, name="save_venture"),
    path("random-ventures", views.generate_random_venture, name="generate_random_venture"),
]
