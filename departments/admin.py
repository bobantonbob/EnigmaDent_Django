from django.contrib import admin
from .models import Articles, ResponseSite


@admin.action(description='Позначити як «Зв’язались»')
def mark_contacted(modeladmin, request, queryset):
    queryset.update(status=Articles.Status.CONTACTED)


@admin.action(description='Позначити як «Запис підтверджено»')
def mark_confirmed(modeladmin, request, queryset):
    queryset.update(status=Articles.Status.CONFIRMED)


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'about', 'status', 'created_at', 'preferred_time')
    list_filter = ('status', 'created_at', 'source')
    search_fields = ('title', 'phone', 'email', 'about', 'message', 'admin_note')
    readonly_fields = ('created_at', 'updated_at', 'source', 'ip_address')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    actions = (mark_contacted, mark_confirmed)
    fieldsets = (
        ('Пацієнт', {'fields': ('title', 'phone', 'email')}),
        ('Запит', {'fields': ('about', 'preferred_time', 'message')}),
        ('Робота із заявкою', {'fields': ('status', 'admin_note')}),
        ('Системна інформація', {'fields': ('created_at', 'updated_at', 'source', 'ip_address'), 'classes': ('collapse',)}),
    )


@admin.register(ResponseSite)
class ResponseSiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'about', 'created_at')
    search_fields = ('title', 'about', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
