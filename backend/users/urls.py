from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, set_pass

router_v1 = DefaultRouter()
router_v1.register(r'users/set_password', set_pass, basename='set_password')
router_v1.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [

    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]
