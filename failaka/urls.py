"""
URL configuration for failakaApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from authentication.views import UserViewset
from entities.views import (
    SiteViewset,
    SubsiteViewset,
    ItemViewset,
    MissionViewset,
    NotableViewset,
    CommentViewset
)


# Initialize routers
userRouter = routers.SimpleRouter()
entitiesRouter = routers.SimpleRouter()

# viewsets with routers
userRouter.register('', UserViewset, basename='user')
entitiesRouter.register('sites', SiteViewset, basename='site')
entitiesRouter.register('subsites', SubsiteViewset, basename='subsite')
entitiesRouter.register('items', ItemViewset, basename='item')
entitiesRouter.register('missions', MissionViewset, basename='mission')
entitiesRouter.register('notables', NotableViewset, basename='notable')
entitiesRouter.register('comments', CommentViewset, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='auth_token'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include(userRouter.urls)),
    path('api/', include(entitiesRouter.urls)),
    path('docs/swagger/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('', include('client.urls')),
]