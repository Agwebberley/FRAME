from django.urls import path
from frame.base_views import (
    HomeView,
    LoginView,
    LogoutView,
    LogMessageView,
    LogMessageDetailView,
    update_field,
    edit_field,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("log/", LogMessageView.as_view(), name="logmessage-list"),
    path("log/<int:pk>/", LogMessageDetailView.as_view(), name="logmessage-detail"),
    path("update-field/", update_field, name="update-field"),
    path("edit-field/", edit_field, name="edit-field"),
]
