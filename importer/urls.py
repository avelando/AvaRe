from django.urls import path
from .views import save_response

urlpatterns = [
    path("save-response/", save_response, name="save-response"),
]
