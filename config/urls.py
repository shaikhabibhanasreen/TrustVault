from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
urlpatterns = [
path("", RedirectView.as_view(url="/accounts/register/", permanent=False), name="home"),
path("admin/", admin.site.urls),
path("accounts/", include("django.contrib.auth.urls")),
path("accounts/", include("accounts.urls")),
path("documents/", include("documents.urls")),
]
