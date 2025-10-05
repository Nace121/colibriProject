from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls", namespace="core")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("students/", include("apps.students.urls", namespace="students")),
    path("companies/", include("apps.companies.urls", namespace="companies")),
    path("teams/", include("apps.teams.urls", namespace="teams")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
