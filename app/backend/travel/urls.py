from django.contrib import admin
from django.urls import include, path

from flights import urls as flights_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(flights_urls)),
]
