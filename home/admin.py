from django.contrib import admin
from .models import GoogleReview, GoogleReviewStats, PriceCategory, PriceItem, Response


@admin.action(description='Опублікувати вибрані відгуки')
def approve_reviews(modeladmin, request, queryset):
    queryset.update(status=Response.ModerationStatus.APPROVED)


@admin.action(description='Приховати вибрані відгуки')
def hide_reviews(modeladmin, request, queryset):
    queryset.update(status=Response.ModerationStatus.HIDDEN)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'timestamp', 'source', 'ip_address')
    list_filter = ('status', 'source', 'timestamp')
    search_fields = ('name', 'email', 'response', 'admin_note')
    readonly_fields = ('timestamp', 'ip_address', 'source')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    actions = (approve_reviews, hide_reviews)
    fieldsets = (
        ('Відгук', {'fields': ('name', 'email', 'response', 'image')}),
        ('Модерація', {'fields': ('status', 'admin_note')}),
        ('Системна інформація', {'fields': ('timestamp', 'source', 'ip_address'), 'classes': ('collapse',)}),
    )


class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 0
    fields = ('code', 'name', 'price', 'price_text', 'note', 'order', 'is_active')
    ordering = ('order', 'id')
    show_change_link = True


@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'order', 'is_active')
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'subtitle')
    list_editable = ('order', 'is_active')
    ordering = ('section', 'order')
    inlines = (PriceItemInline,)


@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'shown_price', 'order', 'is_active')
    list_filter = ('category__section', 'category', 'is_active')
    search_fields = ('code', 'name', 'note')
    list_editable = ('order', 'is_active')
    ordering = ('category__section', 'category__order', 'order')
    autocomplete_fields = ()

    @admin.display(description='Ціна')
    def shown_price(self, obj):
        return obj.display_price


@admin.register(GoogleReview)
class GoogleReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'star_rating', 'short_comment', 'create_time', 'is_visible', 'synced_at')
    list_filter = ('star_rating', 'is_visible', 'create_time')
    search_fields = ('reviewer_name', 'comment', 'reply_comment', 'google_review_id')
    list_editable = ('is_visible',)
    readonly_fields = ('google_review_id', 'synced_at', 'raw_json')
    ordering = ('-create_time', '-id')
    date_hierarchy = 'create_time'

    @admin.display(description='Відгук')
    def short_comment(self, obj):
        value = (obj.comment or '').strip()
        return value[:90] + ('…' if len(value) > 90 else '')


@admin.register(GoogleReviewStats)
class GoogleReviewStatsAdmin(admin.ModelAdmin):
    list_display = ('average_rating', 'total_review_count', 'last_sync_at', 'last_sync_status')
    readonly_fields = ('average_rating', 'total_review_count', 'last_sync_at', 'last_sync_status', 'last_sync_error')
    fields = ('average_rating', 'total_review_count', 'google_maps_url', 'last_sync_at', 'last_sync_status', 'last_sync_error')

    def has_add_permission(self, request):
        return not GoogleReviewStats.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
