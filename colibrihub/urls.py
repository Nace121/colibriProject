
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("apps.core.urls", "core"), namespace="core")),
    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("students/", include(("apps.students.urls", "students"), namespace="students")),
    path("companies/", include(("apps.companies.urls", "companies"), namespace="companies")),
    path("teams/", include(("apps.teams.urls", "teams"), namespace="teams")),
    path("projects/", include(("apps.projects.urls", "projects"), namespace="projects")),
    path("applications/", include(("apps.applications.urls", "applications"), namespace="applications")),
    path("payments/", include(("apps.payments.urls", "payments"), namespace="payments")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)