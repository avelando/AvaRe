from django.urls import path, include
from importer import views as import_views
from compare import views as compare_views

urlpatterns = [
    path("", compare_views.start, name="compare-start"),
    path("compare/", include("compare.urls")),
    path("save_response/", import_views.save_response, name="save-response"),
    path("complete/", import_views.complete, name="complete"),
]
