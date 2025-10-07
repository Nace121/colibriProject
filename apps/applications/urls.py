from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("submit/<uuid:project_id>/", views.submit_application, name="submit"),
    path("mine/", views.my_applications, name="mine"),
    path("project/<uuid:project_id>/", views.project_applications, name="project_list"),
    path("accept/<uuid:application_id>/", views.application_accept, name="accept"),
    path("reject/<uuid:application_id>/", views.application_reject, name="reject"),
]
