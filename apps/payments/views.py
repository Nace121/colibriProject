
import os, json
from decimal import Decimal
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from apps.core.decorators import company_required, student_required
from apps.projects.models import Project
from apps.applications.models import Application
from apps.students.models import Student
from .models import Payment, StudentPayment

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

@login_required
@company_required
def checkout_session_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, company__user=request.user)
    accepted = Application.objects.filter(project=project, status=Application.Status.ACCEPTED).select_related("team").first()
    if not accepted:
        messages.error(request, "Aucune candidature acceptée pour ce projet.")
        return redirect("projects:detail", project_id=project.id)

    if project.status != Project.Status.IN_PROGRESS:
        messages.error(request, "Le projet doit être en cours pour procéder au paiement.")
        return redirect("projects:detail", project_id=project.id)

    amount = project.budget
    if not amount or amount <= 0:
        messages.error(request, "Montant invalide sur le projet.")
        return redirect("projects:detail", project_id=project.id)

    p = Payment.objects.create(
        project=project,
        company=project.company,
        team=accepted.team,
        amount=amount,
        currency="eur",
        status=Payment.Status.PENDING,
    )
    p.compute_fees()
    p.save()

    success_url = request.build_absolute_uri(reverse("payments:success", args=[p.id]))
    cancel_url = request.build_absolute_uri(reverse("payments:cancel", args=[p.id]))

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": p.currency,
                    "product_data": {"name": f"Projet {project.title}"},
                    "unit_amount": int(Decimal(p.amount) * 100),
                },
                "quantity": 1,
            }],
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"payment_id": str(p.id), "project_id": str(project.id)},
        )
        p.stripe_session_id = session.get("id", "")
        p.save()
        return redirect(session.url)
    except Exception as e:
        messages.error(request, f"Erreur Stripe: {e}")
        return redirect("projects:detail", project_id=project.id)

@login_required
def checkout_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payments/success.html", {"payment": payment})

@login_required
def checkout_cancel(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, "payments/cancel.html", {"payment": payment})

def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

    if endpoint_secret:
        try:
            event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=endpoint_secret)
        except Exception as e:
            return HttpResponseBadRequest(f"Signature invalide: {e}")
    else:
        try:
            event = json.loads(payload.decode("utf-8"))
        except Exception as e:
            return HttpResponseBadRequest(f"JSON invalide: {e}")

    event_type = event.get("type")
    data_object = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        payment_id = data_object.get("metadata", {}).get("payment_id")
        if payment_id:
            payment = get_object_or_404(Payment, id=payment_id)
            payment.status = Payment.Status.SUCCEEDED
            payment.stripe_payment_intent_id = data_object.get("payment_intent", "")
            payment.paid_at = timezone.now()
            payment.compute_fees()
            payment.save()

            members = list(payment.team.members.all())
            if members:
                per = (payment.net_amount / Decimal(len(members))).quantize(Decimal("0.01"))
                for m in members:
                    StudentPayment.objects.update_or_create(
                        payment=payment,
                        student=m,
                        defaults={"amount": per, "status": StudentPayment.Status.PAID, "paid_at": timezone.now()},
                    )
    return HttpResponse("OK")

@login_required
@company_required
def company_payments(request):
    from apps.companies.models import Company
    company = get_object_or_404(Company, user=request.user)
    payments = Payment.objects.filter(company=company).select_related("project","team").order_by("-created_at")
    return render(request, "payments/company_list.html", {"payments": payments})

@login_required
@student_required
def student_payments(request):
    student = get_object_or_404(Student, user=request.user)
    sps = student.student_payments.select_related("payment","payment__project").order_by("-paid_at","-payment__created_at")
    return render(request, "payments/student_list.html", {"student_payments": sps})
