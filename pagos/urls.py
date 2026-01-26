from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('', views.pago_list, name='pago_list'),
    path('nuevo/', views.pago_create, name='pago_create'),
    path('nuevo/cliente/<int:cliente_id>/', views.pago_create, name='pago_create_for_cliente'),
    path('<int:pk>/', views.pago_detail, name='pago_detail'),
    path('<int:pk>/editar/', views.pago_update, name='pago_update'),
    path('<int:pk>/eliminar/', views.pago_delete, name='pago_delete'),
    path('<int:pk>/marcar-pagado/', views.pago_marcar_pagado, name='pago_marcar_pagado'),
    
    # Exportación
    path('exportar/excel/', views.pago_exportar_excel, name='pago_exportar_excel'),
    path('exportar/pdf/', views.pago_exportar_pdf, name='pago_exportar_pdf'),
    
    # Calendario y Reportes
    path('calendario/', views.pago_calendario, name='pago_calendario'),
    path('reportes/', views.pago_reportes, name='pago_reportes'),
    
    # API para búsqueda de clientes
    path('api/buscar-clientes/', views.buscar_clientes, name='api_buscar_clientes'),
    path('api/cliente/<int:cliente_id>/instalaciones/', views.obtener_instalaciones_cliente, name='api_instalaciones_cliente'),
]



