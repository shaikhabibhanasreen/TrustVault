
from django.conf import settings
from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    file = models.FileField(upload_to="documents/")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_documents",
    )

    category = models.CharField(
        max_length=100,
        blank=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DocumentPermission(models.Model):
    VIEW = "VIEW"
    EDIT = "EDIT"

    PERMISSION_CHOICES = [
        (VIEW, "View"),
        (EDIT, "Edit"),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="permissions",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="document_permissions",
    )

    permission_type = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES,
        default=VIEW,
    )

    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="granted_document_permissions",
    )

    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "user"],
                name="unique_document_user_permission",
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.document.title} - "
            f"{self.permission_type}"
        )
