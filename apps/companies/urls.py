from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path("me/edit/", views.profile_edit, name="profile_edit"),
    path("<str:username>/", views.profile_view, name="profile_view"),
]
