from django.urls import include, path
from .api.routers import router

urlpatterns = [path("api/", include(router.urls))]
