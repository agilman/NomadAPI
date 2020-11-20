"""nomadapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView

from nomadapp import api
from nomadapp.views import registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico',RedirectView.as_view(url='/user_media/favicon.ico')),
    path('api/rest/user/<str:userName>',api.user),
    path('api/rest/me/<int:userId>',api.me), # path used by editor to get userinfo and adventure info
    path('api/rest/adventures/', api.adventures),  #this is for post
    path('api/rest/adventures/<int:advId>', api.adventures), #this is for delete

    path('api/rest/maps/', api.maps), #this is for post
    path('api/rest/maps/<int:mapId>', api.maps), #this is for delete
    path('api/rest/advMaps/<int:advId>', api.advMaps), #this is for get
    path('api/rest/advMaps2/<int:advId>', api.advMaps2), #this combines map names with segments in one get
    path('api/rest/segments/<int:mapId>', api.segments),
    path('api/rest/photos/photoUpload', api.photoUpload),
    path('api/rest/photos/<int:mapId>', api.photos),

    path("auth/register/", registration, name="registration"),
    path("auth/token/", TokenObtainPairView.as_view(),name="token"),
    path("auth/refresh_token/", TokenRefreshView.as_view(),name="refresh_token"),
]
