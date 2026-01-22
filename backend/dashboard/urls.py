from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import apis, auth_apis

router = DefaultRouter()
router.register(r"ventures", apis.VentureViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "auth/login",
        auth_apis.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
