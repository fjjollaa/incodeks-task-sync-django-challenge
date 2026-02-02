from django.contrib import admin
from django.urls import path, include
from syncapp.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("api/", include("syncapp.urls")),
]
