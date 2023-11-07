from rest_framework.routers import SimpleRouter
from general.views import UserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView
from django.urls import path, include

router = SimpleRouter()
router.register(r'users', UserViewSet, basename="users")

extra_paths = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = router.urls + extra_paths