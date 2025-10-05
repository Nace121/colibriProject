
from django.contrib.auth.decorators import user_passes_test

def is_student(user):
    return user.is_authenticated and getattr(user, "user_type", None) == "STUDENT"

def is_company(user):
    return user.is_authenticated and getattr(user, "user_type", None) == "COMPANY"

student_required = user_passes_test(is_student)
company_required = user_passes_test(is_company)
