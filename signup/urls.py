from django.urls import path
from signup import views

urlpatterns = [path("", views.SignupView.as_view(), name="signup")]
