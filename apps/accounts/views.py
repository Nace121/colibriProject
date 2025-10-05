from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from .forms import RegisterStudentForm, RegisterCompanyForm

def register_student(request):
    if request.method == "POST":
        form = RegisterStudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Compte étudiant créé.")
            return redirect("core:home")
    else:
        form = RegisterStudentForm()
    return render(request, "accounts/register_student.html", {"form": form})

def register_company(request):
    if request.method == "POST":
        form = RegisterCompanyForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Compte entreprise créé.")
            return redirect("core:home")
    else:
        form = RegisterCompanyForm()
    return render(request, "accounts/register_company.html", {"form": form})
