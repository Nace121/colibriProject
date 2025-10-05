from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from .forms import CompanyProfileForm

@login_required
def profile_edit(request):
    company, _ = Company.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CompanyProfileForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect("companies:profile_view", username=request.user.username)
    else:
        form = CompanyProfileForm(instance=company)
    return render(request, "companies/profile_edit.html", {"form": form})

def profile_view(request, username):
    company = get_object_or_404(Company, user__username=username)
    return render(request, "companies/profile_view.html", {"company": company})
