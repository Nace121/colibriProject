
from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/<uuid:project_id>/", views.checkout_session_create, name="checkout"),
    path("success/<uuid:payment_id>/", views.checkout_success, name="success"),
    path("cancel/<uuid:payment_id>/", views.checkout_cancel, name="cancel"),
    path("webhook/stripe/", views.stripe_webhook, name="webhook"),
    path("company/", views.company_payments, name="company_list"),
    path("student/", views.student_payments, name="student_list"),
]
