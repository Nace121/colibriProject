from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentProfileForm

@login_required
def profile_edit(request):
    student, _ = Student.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect("students:profile_view", username=request.user.username)
    else:
        form = StudentProfileForm(instance=student)
    return render(request, "students/profile_edit.html", {"form": form})

def profile_view(request, username):
    student = get_object_or_404(Student, user__username=username)
    return render(request, "students/profile_view.html", {"student": student})
