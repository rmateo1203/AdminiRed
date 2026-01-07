from django.urls import path
from . import views
from . import catalogos_views

app_name = 'core'

urlpatterns = [
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
]

