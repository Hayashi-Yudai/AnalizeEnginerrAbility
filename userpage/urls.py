from django.urls import path
from userpage import views

urlpatterns = [path("", views.index, name="userpage")]
