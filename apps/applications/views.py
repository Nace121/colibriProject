
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.core.decorators import student_required, company_required
from apps.projects.models import Project
from apps.teams.models import Team
from .models import Application
from .forms import ApplicationCreateForm

@login_required
@student_required
def submit_application(request, project_id):
    project = get_object_or_404(Project, id=project_id, status=Project.Status.PUBLISHED)
    if request.method == "POST":
        form = ApplicationCreateForm(request.POST, user=request.user)
        if form.is_valid():
            app = form.save(commit=False)
            # Security checks
            if not app.team.members.filter(user=request.user).exists():
                messages.error(request, "Tu dois appartenir à l'équipe sélectionnée.")
                return redirect("applications:submit", project_id=project.id)
            if Application.objects.filter(project=project, team=app.team).exists():
                messages.info(request, "Cette équipe a déjà candidaté pour ce projet.")
                return redirect("projects:detail", project_id=project.id)
            app.project = project
            app.save()
            form.save_m2m()
            messages.success(request, "Candidature envoyée.")
            return redirect("applications:mine")
    else:
        form = ApplicationCreateForm(user=request.user)
    return render(request, "applications/submit.html", {"form": form, "project": project})

@login_required
@student_required
def my_applications(request):
    # All applications for teams where the user is a member
    teams = Team.objects.filter(members__user=request.user).distinct()
    apps = Application.objects.filter(team__in=teams).select_related("project","team")
    return render(request, "applications/my_list.html", {"applications": apps})

@login_required
@company_required
def project_applications(request, project_id):
    project = get_object_or_404(Project, id=project_id, company__user=request.user)
    apps = project.applications.select_related("team").all()
    return render(request, "applications/project_list.html", {"project": project, "applications": apps})

@login_required
@company_required
def application_accept(request, application_id):
    app = get_object_or_404(Application, id=application_id, project__company__user=request.user)
    project = app.project

    # Optionally prevent multiple acceptances
    if app.status == Application.Status.ACCEPTED:
        messages.info(request, "Cette candidature est déjà acceptée.")
        return redirect("applications:project_list", project_id=project.id)

    # Accept this application
    app.status = Application.Status.ACCEPTED
    app.reviewed_at = timezone.now()
    app.save()

    # Reject others for the same project
    Application.objects.filter(project=project).exclude(id=app.id).update(
        status=Application.Status.REJECTED, reviewed_at=timezone.now()
    )

    # Set project status and assigned team if available
    try:
        from apps.projects.models import Project as ProjectModel
        from apps.teams.models import Team as TeamModel
        # Add assigned_team only if the field exists
        if hasattr(project, "assigned_team_id"):
            project.assigned_team_id = app.team.id
        project.status = ProjectModel.Status.IN_PROGRESS
        project.save()
    except Exception:
        # Do not block accept if field not present
        project.status = project.Status.IN_PROGRESS
        project.save()

    messages.success(request, "Candidature acceptée. Projet en cours.")
    return redirect("applications:project_list", project_id=project.id)

@login_required
@company_required
def application_reject(request, application_id):
    app = get_object_or_404(Application, id=application_id, project__company__user=request.user)
    if app.status in [Application.Status.REJECTED]:
        messages.info(request, "Cette candidature est déjà refusée.")
    else:
        app.status = Application.Status.REJECTED
        app.reviewed_at = timezone.now()
        app.save()
        messages.success(request, "Candidature refusée.")
    return redirect("applications:project_list", project_id=app.project.id)
