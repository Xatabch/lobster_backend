from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserSignup.as_view(), name="user-signup"),
    path("profile/", views.Profile.as_view(), name="profile"),
    path("test/", views.test, name="test")
]