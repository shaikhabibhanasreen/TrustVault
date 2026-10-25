from django.conf import settings
from django.db import models


class AuditLog(models.Model):

    ACTION_CHOICES = [
        ("UPLOAD", "Document Uploaded"),
        ("VIEW", "Document Viewed"),
        ("DOWNLOAD", "Document Downloaded"),
        ("EDIT", "Document Edited"),
        ("DELETE", "Document Deleted"),
        ("PERMISSION_GRANTED", "Permission Granted"),
        ("PERMISSION_REVOKED", "Permission Revoked"),
        ("ACCESS_DENIED", "Access Denied"),
    ]

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES,
    )

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    details = models.JSONField(default=dict, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    previous_hash = models.CharField(
        max_length=64,
        blank=True,
        default="",
    )

    entry_hash = models.CharField(
        max_length=64,
        blank=True,
        default="",
    )

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action} - {self.timestamp}"