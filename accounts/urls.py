from django.urls import path

from accounts.views import (
    ClientDetailView,
    ClientUpdateView,
    ClientSignUpView,
    UserDetailView,
    AdminDetailView,
    AdminSignUpView,
    AdminUpdateView,
    dashboard,
)

app_name = "accounts"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("signup/", ClientSignUpView.as_view(), name="signup-client"),
    path("admin/signup/", AdminSignUpView.as_view(), name="admin-signup"),
    path("profile/<str:pk>/client/", ClientDetailView.as_view(), name="client-profile"),
    path("profile/<str:pk>/admin/", AdminDetailView.as_view(), name="admin-profile"),
    path("update/<str:pk>/client/", ClientUpdateView.as_view(), name="client-update"),
    path("update/<str:pk>/admin/", AdminUpdateView.as_view(), name="admin-update"),
    path("detail/<str:pk>/", UserDetailView.as_view(), name="user-detail"),
]
