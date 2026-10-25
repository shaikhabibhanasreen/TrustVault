
from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "actor",
        "action",
        "document",
        "previous_hash",
        "entry_hash",
    )

    list_filter = (
        "action",
        "timestamp",
    )

    search_fields = (
        "actor__username",
        "document__title",
        "action",
    )

    readonly_fields = (
        "actor",
        "action",
        "document",
        "details",
        "timestamp",
        "previous_hash",
        "entry_hash",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False