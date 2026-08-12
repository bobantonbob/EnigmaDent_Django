from django.contrib import admin

from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'issuer', 'issued_at', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'issued_at')
    search_fields = ('title', 'issuer', 'description')
    list_editable = ('order', 'is_active')
    ordering = ('order', '-issued_at', '-created_at')
