from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserSignup.as_view(), name="user-signup"),
    path("profile/", views.UserProfile.as_view(), name="user-profile")
]