from django.urls import path

from general.views import (
    UserViewSet,
    ClassGroupViewSet,
    CustomTokenObtainPairView,
    CustomTokenRefreshView
    )

urlpatterns = [
    path('user', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('user/<int:pk>', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'})),
    path('user/me', UserViewSet.as_view({'get': 'me'})),
    path('user/import', UserViewSet.as_view({'post': 'user_import'})),
    path('user/<int:pk>/photo', UserViewSet.as_view({'post': 'upload_photo'})),
    path('group/', ClassGroupViewSet.as_view({'get': 'list'})),
    path('group/<int:pk>', ClassGroupViewSet.as_view({'get': 'retrieve'})),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]