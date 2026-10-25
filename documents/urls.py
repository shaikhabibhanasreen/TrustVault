from django.urls import path
from . import views

urlpatterns = [
path("dashboard/", views.dashboard, name="dashboard"),
path("upload/", views.upload_document, name="upload_document"),
path("list/", views.document_list, name="document_list"),
path("view/<int:document_id>/", views.view_document, name="view_document"),
path("share/<int:document_id>/", views.share_document, name="share_document"),
path(
    "revoke/<int:document_id>/<int:user_id>/",
    views.revoke_permission,
    name="revoke_permission",
),
]
