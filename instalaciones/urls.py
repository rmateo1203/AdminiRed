from django.urls import path
from . import views

app_name = 'instalaciones'

urlpatterns = [
    path('', views.instalacion_list, name='instalacion_list'),
    path('nueva/', views.instalacion_create, name='instalacion_create'),
    path('nueva/cliente/<int:cliente_id>/', views.instalacion_create, name='instalacion_create_for_cliente'),
    path('<int:pk>/', views.instalacion_detail, name='instalacion_detail'),
    path('<int:pk>/editar/', views.instalacion_update, name='instalacion_update'),
    path('<int:pk>/eliminar/', views.instalacion_delete, name='instalacion_delete'),
    path('api/plan/<int:plan_id>/', views.get_plan_data, name='get_plan_data'),
    
    # API para búsqueda de clientes
    path('api/buscar-clientes/', views.buscar_clientes_api, name='api_buscar_clientes'),
    path('api/cliente/<int:cliente_id>/instalaciones/', views.get_cliente_instalaciones_api, name='api_instalaciones_cliente'),
    
    # Configuración de número de contrato
    path('configurar-numero-contrato/', views.configurar_numero_contrato, name='configurar_numero_contrato'),
    path('api/preview-numero-contrato/', views.preview_numero_contrato, name='api_preview_numero_contrato'),
]

