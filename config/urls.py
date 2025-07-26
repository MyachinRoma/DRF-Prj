from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("materials/courses/", include("materials.urls", namespace="courses")),
    path("materials/lessons/", include("materials.urls", namespace="lessons")),
]
