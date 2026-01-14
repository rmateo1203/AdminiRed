from django.urls import path
from . import views
from . import catalogos_views
from . import roles_views
from . import realtime_views

app_name = 'core'

urlpatterns = [
    # Error de permisos
    path('sin-permisos/', views.sin_permisos, name='sin_permisos'),
    # Roles y Permisos
    path('roles/', roles_views.roles_dashboard, name='roles_dashboard'),
    path('roles/lista/', roles_views.roles_list, name='roles_list'),
    path('roles/crear/', roles_views.rol_create, name='rol_create'),
    path('roles/<int:pk>/', roles_views.rol_detail, name='rol_detail'),
    path('roles/<int:pk>/editar/', roles_views.rol_update, name='rol_update'),
    path('roles/<int:pk>/permisos/', roles_views.rol_permisos_update, name='rol_permisos_update'),
    path('permisos/', roles_views.permisos_list, name='permisos_list'),
    path('permisos/crear/', roles_views.permiso_create, name='permiso_create'),
    path('permisos/<int:pk>/', roles_views.permiso_detail, name='permiso_detail'),
    path('permisos/<int:pk>/editar/', roles_views.permiso_update, name='permiso_update'),
    path('usuarios/roles/', roles_views.usuarios_roles_list, name='usuarios_roles_list'),
    path('usuarios/crear/', roles_views.usuario_create, name='usuario_create'),
    path('usuarios/<int:user_id>/editar/', roles_views.usuario_update, name='usuario_update'),
    path('usuarios/<int:user_id>/roles/', roles_views.usuario_roles_manage, name='usuario_roles_manage'),
    # Catálogos
    path('catalogos/', catalogos_views.catalogos_dashboard, name='catalogos_dashboard'),
    
    # Tipos de Instalación
    path('catalogos/tipos-instalacion/', catalogos_views.catalogo_tipo_instalacion_list, name='catalogo_tipo_instalacion_list'),
    path('catalogos/tipos-instalacion/crear/', catalogos_views.catalogo_tipo_instalacion_create, name='catalogo_tipo_instalacion_create'),
    path('catalogos/tipos-instalacion/<int:pk>/editar/', catalogos_views.catalogo_tipo_instalacion_update, name='catalogo_tipo_instalacion_update'),
    path('catalogos/tipos-instalacion/<int:pk>/eliminar/', catalogos_views.catalogo_tipo_instalacion_delete, name='catalogo_tipo_instalacion_delete'),
    
    # Planes de Internet
    path('catalogos/planes-internet/', catalogos_views.catalogo_plan_internet_list, name='catalogo_plan_internet_list'),
    path('catalogos/planes-internet/crear/', catalogos_views.catalogo_plan_internet_create, name='catalogo_plan_internet_create'),
    path('catalogos/planes-internet/<int:pk>/editar/', catalogos_views.catalogo_plan_internet_update, name='catalogo_plan_internet_update'),
    path('catalogos/planes-internet/<int:pk>/eliminar/', catalogos_views.catalogo_plan_internet_delete, name='catalogo_plan_internet_delete'),
    
    # Categorías de Material
    path('catalogos/categorias-material/', catalogos_views.catalogo_categoria_material_list, name='catalogo_categoria_material_list'),
    path('catalogos/categorias-material/crear/', catalogos_views.catalogo_categoria_material_create, name='catalogo_categoria_material_create'),
    path('catalogos/categorias-material/<int:pk>/editar/', catalogos_views.catalogo_categoria_material_update, name='catalogo_categoria_material_update'),
    path('catalogos/categorias-material/<int:pk>/eliminar/', catalogos_views.catalogo_categoria_material_delete, name='catalogo_categoria_material_delete'),
    
    # Tipos de Notificación
    path('catalogos/tipos-notificacion/', catalogos_views.catalogo_tipo_notificacion_list, name='catalogo_tipo_notificacion_list'),
    path('catalogos/tipos-notificacion/crear/', catalogos_views.catalogo_tipo_notificacion_create, name='catalogo_tipo_notificacion_create'),
    path('catalogos/tipos-notificacion/<int:pk>/editar/', catalogos_views.catalogo_tipo_notificacion_update, name='catalogo_tipo_notificacion_update'),
    path('catalogos/tipos-notificacion/<int:pk>/eliminar/', catalogos_views.catalogo_tipo_notificacion_delete, name='catalogo_tipo_notificacion_delete'),
    
    # Configuración del Sistema
    path('configurar-sistema/', views.configurar_sistema, name='configurar_sistema'),
    
    # Actualizaciones en tiempo real
    path('realtime/check-updates/', realtime_views.check_updates, name='check_updates'),
    path('realtime/updates/<str:model_name>/', realtime_views.get_model_updates, name='get_model_updates'),
]

