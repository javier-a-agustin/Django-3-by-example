from django.contrib import admin
from django.urls import path, include


def my_error(request):
    1 / 0


urlpatterns = [
    path("admin/", admin.site.urls),
    path("my_error/", my_error),
    path("blog/", include("blog.urls", namespace="blog")),
]
