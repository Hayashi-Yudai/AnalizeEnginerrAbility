from django.urls import path
from userpage import views

urlpatterns = [path("", views.Index.as_view(), name="userpage")]
