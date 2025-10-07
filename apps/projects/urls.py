
from django.urls import path
from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="list"),
    path("create/", views.project_create, name="create"),
    path("mine/", views.my_projects, name="my_projects"),
    path("<uuid:project_id>/", views.project_detail, name="detail"),
]
