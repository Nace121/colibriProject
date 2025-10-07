
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from apps.core.decorators import company_required
from apps.companies.models import Company
from apps.students.models import Skill
from .models import Project
from .forms import ProjectForm

@login_required
@company_required
def project_create(request):
    company, _ = Company.objects.get_or_create(user=request.user, defaults={"company_name": request.user.username})
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.company = company
            project.save()
            form.save_m2m()
            messages.success(request, "Projet créé.")
            return redirect("projects:my_projects")
    else:
        form = ProjectForm()
    return render(request, "projects/create.html", {"form": form})

@login_required
@company_required
def my_projects(request):
    company = get_object_or_404(Company, user=request.user)
    qs = company.projects.order_by("-created_at")
    return render(request, "projects/my_list.html", {"projects": qs})

@login_required
def project_list(request):
    qs = Project.objects.filter(status=Project.Status.PUBLISHED).order_by("-published_at", "-created_at")

    q = request.GET.get("q") or ""
    category = request.GET.get("category") or ""
    budget_min = request.GET.get("budget_min") or ""
    budget_max = request.GET.get("budget_max") or ""
    skill_ids = request.GET.getlist("skills")

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
    if category:
        qs = qs.filter(category=category)
    if budget_min:
        try:
            qs = qs.filter(budget__gte=float(budget_min))
        except ValueError:
            pass
    if budget_max:
        try:
            qs = qs.filter(budget__lte=float(budget_max))
        except ValueError:
            pass
    if skill_ids:
        qs = qs.filter(required_skills__in=skill_ids).distinct()

    skills = Skill.objects.all().order_by("name")
    return render(request, "projects/list.html", {
        "projects": qs,
        "skills": skills,
        "q": q,
        "category": category,
        "budget_min": budget_min,
        "budget_max": budget_max,
        "selected_skills": [int(s) for s in skill_ids] if skill_ids else [],
    })

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, "projects/detail.html", {"project": project})
