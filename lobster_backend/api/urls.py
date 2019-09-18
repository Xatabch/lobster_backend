from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserSignup.as_view(), name="user-signup"),
    path("test/", views.test, name="test")
]