from django.urls import path
from . import views

app_name = 'pagos'

urlpatterns = [
    path('', views.pago_list, name='pago_list'),
    path('pendientes/', views.pago_pendientes_list, name='pago_pendientes_list'),
    path('vencidos/', views.pago_vencidos_list, name='pago_vencidos_list'),
    path('nuevo/', views.pago_create, name='pago_create'),
    path('nuevo/cliente/<int:cliente_id>/', views.pago_create, name='pago_create_for_cliente'),
    path('registro-manual/', views.pago_registro_manual, name='pago_registro_manual'),
    path('registro-manual/cliente/<int:cliente_id>/', views.pago_registro_manual, name='pago_registro_manual_for_cliente'),
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
    
    # Pasarela de pago
    path('<int:pk>/pagar-online/', views.pago_procesar_online, name='pago_procesar_online'),
    path('<int:pk>/pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('<int:pk>/pago-cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('webhook/mercadopago/', views.mercadopago_webhook, name='mercadopago_webhook'),
    
    # Reembolsos
    path('transaccion/<int:transaccion_id>/reembolsar/', views.pago_reembolsar, name='pago_reembolsar'),
    
    # Planes de Pago
    path('planes-pago/', views.plan_pago_list, name='plan_pago_list'),
    path('planes-pago/nuevo/', views.plan_pago_create, name='plan_pago_create'),
    path('planes-pago/nuevo/instalacion/<int:instalacion_id>/', views.plan_pago_create, name='plan_pago_create_for_instalacion'),
    path('planes-pago/<int:pk>/', views.plan_pago_detail, name='plan_pago_detail'),
    path('planes-pago/<int:pk>/editar/', views.plan_pago_update, name='plan_pago_update'),
    path('planes-pago/<int:pk>/eliminar/', views.plan_pago_delete, name='plan_pago_delete'),
]



