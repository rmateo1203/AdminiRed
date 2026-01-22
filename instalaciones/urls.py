from django.urls import path
from . import views, views_materiales

app_name = 'instalaciones'

urlpatterns = [
    path('', views.instalacion_list, name='instalacion_list'),
    path('nueva/', views.instalacion_create, name='instalacion_create'),
    path('nueva/cliente/<int:cliente_id>/', views.instalacion_create, name='instalacion_create_for_cliente'),
    path('<int:pk>/', views.instalacion_detail, name='instalacion_detail'),
    path('<int:pk>/editar/', views.instalacion_update, name='instalacion_update'),
    path('<int:pk>/eliminar/', views.instalacion_delete, name='instalacion_delete'),
    path('<int:pk>/cambiar-estado/', views.instalacion_cambiar_estado, name='instalacion_cambiar_estado'),
    path('<int:pk>/seguimiento-rapido/', views.instalacion_seguimiento_rapido, name='instalacion_seguimiento_rapido'),
    path('api/plan/<int:plan_id>/', views.get_plan_data, name='get_plan_data'),
    
    # API para búsqueda de clientes
    path('api/buscar-clientes/', views.buscar_clientes_api, name='api_buscar_clientes'),
    path('api/cliente/<int:cliente_id>/instalaciones/', views.get_cliente_instalaciones_api, name='api_instalaciones_cliente'),
    
    # Gestión de materiales
    path('<int:instalacion_id>/materiales/', views_materiales.gestionar_materiales, name='gestionar_materiales'),
    path('api/material-info/<int:material_id>/', views_materiales.get_material_info, name='get_material_info'),
]

