from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DocumentPermissionForm, DocumentUploadForm
from .models import Document, DocumentPermission
from audit.services import create_audit_log
from audit.models import AuditLog
@login_required
def upload_document(request):
    if request.user.role.strip().upper() not in ("OWNER", "ADMIN"):
        create_audit_log(
        actor=request.user,
        action="ACCESS_DENIED",
        details={"operation": "UPLOAD"},
        )
        return HttpResponseForbidden(
        "Access denied. Only Owners and Admins can upload documents."
        )

    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user
            document.save()

        create_audit_log(
            actor=request.user,
            action="UPLOAD",
            document=document,
            details={
                "title": document.title,
                "category": document.category,
            },
        )

        return redirect("document_list")

    else:
        form = DocumentUploadForm()
    return render(
    request,
    "documents/upload.html",
    {"form": form},
)

@login_required
def document_list(request):
    search_query = request.GET.get("q", "").strip()

    documents = Document.objects.filter(
        Q(owner=request.user)
        | Q(permissions__user=request.user)
    ).distinct()

    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__icontains=search_query)
        )

    documents = documents.order_by("-uploaded_at")

    return render(
        request,
        "documents/list.html",
        {
            "documents": documents,
            "search_query": search_query,
        },
    )

@login_required
def view_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Check document ownership
    is_owner = document.owner_id == request.user.id

    # Check document-sharing permissions
    has_permission = document.permissions.filter(
        user=request.user,
        permission_type__in=["VIEW", "EDIT"],
    ).exists()

# Debug information
    print(
        "DEBUG:",
        request.user.username,
        request.user.id,
        document.owner_id,
        is_owner,
        has_permission,
    )

# Deny access if the user is not the owner and has no permission
    if not is_owner and not has_permission:
        create_audit_log(
            actor=request.user,
            action="ACCESS_DENIED",
            document=document,
            details={"operation": "VIEW"},
        )

        return HttpResponseForbidden(
            "Access denied. You do not have permission to view this document."
        )

    create_audit_log(
            actor=request.user,
            action="VIEW",
            document=document,
            details={"operation": "VIEW"},
        )

        # Return the document file
    return FileResponse(
            document.file.open("rb"),
            as_attachment=False,
            filename=document.file.name.split("/")[-1],
        )
@login_required
def share_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

# Only the owner or an Admin can share the document
    if (
    document.owner_id != request.user.id
    and request.user.role.strip().upper() != "ADMIN"
):
        create_audit_log(
        actor=request.user,
        action="ACCESS_DENIED",
        document=document,
        details={"operation": "SHARE"},
    )
        return HttpResponseForbidden(
        "Access denied. Only the document owner or an Admin can share it."
    )

    if request.method == "POST":
        form = DocumentPermissionForm(request.POST)

        if form.is_valid():
            permission = form.save(commit=False)
            permission.document = document
            permission.granted_by = request.user

        # Prevent granting permission to the document owner
            if permission.user_id == document.owner_id:
                form.add_error(
                    "user",
                    "The document owner already has access.",
                )
            else:
                permission.save()

            create_audit_log(
                actor=request.user,
                action="PERMISSION_GRANTED",
                document=document,
                details={
                    "shared_with": permission.user.username,
                    "permission_type": permission.permission_type,
                },
            )

            return redirect("document_list")
    else:
        form = DocumentPermissionForm()

    return render(
    request,
    "documents/share.html",
    {
        "form": form,
        "document": document,
    },
)
@login_required
@require_POST
def revoke_permission(request, document_id, user_id):
# Step 1: Find the document
    document = get_object_or_404(Document, id=document_id)


# Step 2: Only the document owner or an Admin can revoke access
    if (
    document.owner_id != request.user.id
    and request.user.role.strip().upper() != "ADMIN"
):
        create_audit_log(
        actor=request.user,
        action="ACCESS_DENIED",
        document=document,
        details={"operation": "REVOKE_PERMISSION"},
    )

        return HttpResponseForbidden(
        "Access denied. Only the document owner or an Admin can revoke permissions."
    )

# Step 3: Find the permission to revoke
    permission = DocumentPermission.objects.filter(
    document=document,
    user_id=user_id,
).first()

# Step 4: Check whether the permission exists
    if permission is None:
        return render(
            request,
            "documents/revoke_result.html",
            {
                "document": document,
                "message": "No permission exists for this user on this document.",
            },
        )
# Step 5: Store information before deleting the permission
    username = permission.user.username
    permission_type = permission.permission_type

        # Step 6: Remove the permission
    permission.delete()

# Step 7: Record the revocation in the audit log
    create_audit_log(
    actor=request.user,
    action="PERMISSION_REVOKED",
    document=document,
    details={
        "revoked_from": username,
        "permission_type": permission_type,
    },
)

# Step 8: Display the result
    return render(
    request,
    "documents/revoke_result.html",
    {
        "document": document,
        "message": f"Access revoked successfully for {username}.",
    },
)
@login_required
def dashboard(request):
    if request.user.role.strip().upper() == "ADMIN":
        documents = Document.objects.all()
        audit_logs = AuditLog.objects.all()
        total_users = User.objects.count()
    else:
        documents = Document.objects.filter(
            Q(owner=request.user)
            | Q(permissions__user=request.user)
        ).distinct()

        audit_logs = AuditLog.objects.filter(
            Q(actor=request.user)
            | Q(document__owner=request.user)
        ).distinct()

        total_users = None

    total_documents = documents.count()

    if request.user.role.strip().upper() == "ADMIN":
        total_permissions = DocumentPermission.objects.count()
        access_denied_count = AuditLog.objects.filter(
            action="ACCESS_DENIED"
        ).count()
    else:
        total_permissions = DocumentPermission.objects.filter(
            document__owner=request.user
        ).count()

        access_denied_count = audit_logs.filter(
            action="ACCESS_DENIED"
        ).count()

    recent_activity = audit_logs.order_by("-timestamp")[:10]

    context = {
        "total_documents": total_documents,
        "total_users": total_users,
        "total_permissions": total_permissions,
        "access_denied_count": access_denied_count,
        "recent_activity": recent_activity,
    }

    return render(
        request,
        "documents/dashboard.html",
        context,
    )