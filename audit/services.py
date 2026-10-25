
import hashlib
import json

from django.db import transaction

from .models import AuditLog


def create_audit_log(
    actor,
    action,
    document=None,
    details=None,
):
    """
    Create an audit log entry linked to the previous entry.
    """

    with transaction.atomic():
        last_log = (
            AuditLog.objects
            .select_for_update()
            .order_by("-id")
            .first()
        )

        previous_hash = last_log.entry_hash if last_log else ""

        timestamp = transaction.get_connection().ops.adapt_datetimefield_value(
            None
        ) if False else None

        log = AuditLog(
            actor=actor,
            action=action,
            document=document,
            details=details or {},
            previous_hash=previous_hash,
        )

        log.save()

        hash_payload = {
            "id": log.id,
            "actor_id": log.actor_id,
            "action": log.action,
            "document_id": log.document_id,
            "details": log.details,
            "timestamp": log.timestamp.isoformat(),
            "previous_hash": log.previous_hash,
        }

        serialized_payload = json.dumps(
            hash_payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        log.entry_hash = hashlib.sha256(
            serialized_payload.encode("utf-8")
        ).hexdigest()

        log.save(update_fields=["entry_hash"])

        return log

def verify_audit_chain():
    """
    Verify audit entry hashes and previous-hash links.
    Returns (is_valid, message).
    """

    logs = AuditLog.objects.order_by("id")
    expected_previous_hash = ""

    for log in logs:
        if log.previous_hash != expected_previous_hash:
            return (
                False,
                f"Previous-hash mismatch at audit log ID {log.id}",
            )

        hash_payload = {
            "id": log.id,
            "actor_id": log.actor_id,
            "action": log.action,
            "document_id": log.document_id,
            "details": log.details,
            "timestamp": log.timestamp.isoformat(),
            "previous_hash": log.previous_hash,
        }

        serialized_payload = json.dumps(
            hash_payload,
            sort_keys=True,
            separators=(",", ":"),
        )

        calculated_hash = hashlib.sha256(
            serialized_payload.encode("utf-8")
        ).hexdigest()

        if log.entry_hash != calculated_hash:
            return (
                False,
                f"Entry hash mismatch at audit log ID {log.id}",
            )

        expected_previous_hash = log.entry_hash

    return True, "Audit chain is valid."
 