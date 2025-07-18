"""
URL configuration for backend project.

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
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/', include('general.urls')),
    path('api/', include('apps.curriculum.urls')),
    path('api/', include('apps.units.pyp.urls')),
    path('api/', include('apps.units.myp.urls')),
    path('api/', include('apps.units.dp.urls')),
    path('api/', include('apps.report.urls')),
    path('api/', include('apps.ibo.urls')),
    path('api/', include('apps.syllabus.urls')),
    path('api/', include('apps.portfolio.urls')),
]

if bool(settings.DEBUG):
    import debug_toolbar
    urlpatterns += [ path('__debug__/', include(debug_toolbar.urls)) ]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)