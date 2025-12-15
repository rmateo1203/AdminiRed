"""
URL configuration for adminired project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, logout_view, toggle_sidebar, config_sidebar

urlpatterns = [
    path('', home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('toggle-sidebar/', toggle_sidebar, name='toggle_sidebar'),
    path('config/sidebar/', config_sidebar, name='config_sidebar'),
    path('', include('core.urls')),
    path('clientes/', include('clientes.urls')),
    path('instalaciones/', include('instalaciones.urls')),
    path('pagos/', include('pagos.urls')),
    path('inventario/', include('inventario.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('admin/', admin.site.urls),
]

# Servir archivos estáticos y medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
