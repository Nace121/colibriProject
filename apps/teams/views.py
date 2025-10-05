
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from apps.core.decorators import student_required
from apps.students.models import Student
from .models import Team, TeamInvitation
from .forms import TeamCreateForm, TeamInviteForm

@login_required
@student_required
def team_list(request):
    student = get_object_or_404(Student, user=request.user)
    teams = Team.objects.filter(members=student).order_by("-created_at")
    return render(request, "teams/list.html", {"teams": teams})

@login_required
@student_required
def team_create(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.leader = student
            team.save()
            team.members.add(student)
            messages.success(request, "Équipe créée.")
            return redirect("teams:detail", team_id=team.id)
    else:
        form = TeamCreateForm()
    return render(request, "teams/create.html", {"form": form})

@login_required
@student_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, "teams/detail.html", {"team": team})

@login_required
@student_required
def team_invite(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    student = get_object_or_404(Student, user=request.user)
    if team.leader != student:
        messages.error(request, "Seul le leader peut inviter des membres.")
        return redirect("teams:detail", team_id=team.id)

    if request.method == "POST":
        form = TeamInviteForm(request.POST)
        if form.is_valid():
            invitee = form.cleaned_data["student"]
            if team.members.count() >= 4:
                messages.error(request, "Équipe déjà complète.")
            elif invitee in team.members.all():
                messages.info(request, "Cet étudiant est déjà membre.")
            else:
                inv, created = TeamInvitation.objects.get_or_create(team=team, student=invitee)
                if created:
                    messages.success(request, "Invitation envoyée.")
                else:
                    messages.info(request, "Invitation déjà existante.")
            return redirect("teams:detail", team_id=team.id)
    else:
        form = TeamInviteForm()
    return render(request, "teams/invite.html", {"team": team, "form": form})

@login_required
@student_required
def invitation_respond(request, invitation_id, action):
    invitation = get_object_or_404(TeamInvitation, id=invitation_id)
    student = get_object_or_404(Student, user=request.user)
    if invitation.student != student:
        messages.error(request, "Tu ne peux pas répondre à cette invitation.")
        return redirect("teams:list")

    if action == "accept":
        if invitation.team.members.count() >= 4:
            messages.error(request, "Impossible d'accepter, l'équipe est complète.")
        else:
            invitation.status = TeamInvitation.Status.ACCEPTED
            invitation.responded_at = timezone.now()
            invitation.save()
            invitation.team.members.add(student)
            messages.success(request, "Invitation acceptée.")
    elif action == "refuse":
        invitation.status = TeamInvitation.Status.REFUSED
        invitation.responded_at = timezone.now()
        invitation.save()
        messages.info(request, "Invitation refusée.")
    else:
        messages.error(request, "Action invalide.")

    return redirect("teams:list")
