from django.urls import path
from .views import compare_detail

urlpatterns = [
    path("questions/", compare_detail, name="compare-detail"),
]
