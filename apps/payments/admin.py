
from django.contrib import admin
from .models import Payment, StudentPayment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("project","company","team","amount","platform_fee","net_amount","status","created_at","paid_at")
    list_filter = ("status",)
    search_fields = ("project__title","company__company_name","team__name","stripe_payment_intent_id")

@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_display = ("payment","student","amount","status","paid_at")
    list_filter = ("status",)
    search_fields = ("student__user__username","payment__project__title")
