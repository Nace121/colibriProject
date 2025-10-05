
from django.urls import path
from . import views

app_name = "teams"

urlpatterns = [
    path("", views.team_list, name="list"),
    path("create/", views.team_create, name="create"),
    path("<uuid:team_id>/", views.team_detail, name="detail"),
    path("<uuid:team_id>/invite/", views.team_invite, name="invite"),
    path("invitation/<int:invitation_id>/<str:action>/", views.invitation_respond, name="invitation_respond"),
]
