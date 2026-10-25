
from django.contrib import admin
from .models import Document, DocumentPermission


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "owner",
        "category",
        "uploaded_at",
        "updated_at",
    )

    list_filter = (
        "category",
        "uploaded_at",
    )

    search_fields = (
        "title",
        "description",
        "owner__username",
    )

    readonly_fields = (
        "uploaded_at",
        "updated_at",
    )


@admin.register(DocumentPermission)
class DocumentPermissionAdmin(admin.ModelAdmin):
    list_display = (
        "document",
        "user",
        "permission_type",
        "granted_by",
        "granted_at",
    )

    list_filter = (
        "permission_type",
        "granted_at",
    )

    search_fields = (
        "document__title",
        "user__username",
        "granted_by__username",
    )

    readonly_fields = (
        "granted_at",
    )