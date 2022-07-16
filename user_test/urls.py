from django.urls import path
from .views import *

app_name = "user_test"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("test/<int:pk>/", TestView.as_view(), name="test"),
]
