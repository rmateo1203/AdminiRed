from django.urls import path
from . import views
from . import portal_views

app_name = 'clientes'

urlpatterns = [
    # URLs del admin (requieren login de staff)
    path('', views.cliente_list, name='cliente_list'),
    path('nuevo/', views.cliente_create, name='cliente_create'),
    path('<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
    path('<int:pk>/restaurar/', views.cliente_restore, name='cliente_restore'),
    path('<int:pk>/crear-usuario-portal/', views.cliente_crear_usuario_portal, name='cliente_crear_usuario_portal'),
    path('cambiar-password/<str:cliente_ids>/', views.cliente_cambiar_password, name='cambiar_password'),
    # Exportación e importación
    path('exportar/excel/', views.cliente_exportar_excel, name='cliente_exportar_excel'),
    path('exportar/pdf/', views.cliente_exportar_pdf, name='cliente_exportar_pdf'),
    path('importar/', views.cliente_importar_excel, name='cliente_importar_excel'),
    # Bulk actions
    path('bulk-action/', views.cliente_bulk_action, name='cliente_bulk_action'),
    # API endpoints
    path('api/verificar-duplicado/', views.cliente_verificar_duplicado, name='cliente_verificar_duplicado'),
    
    # URLs del portal de clientes
    path('portal/registro/', portal_views.portal_registro, name='portal_registro'),
    path('portal/login/', portal_views.portal_login, name='portal_login'),
    path('portal/', portal_views.portal_dashboard, name='portal_dashboard'),
    path('portal/mis-pagos/', portal_views.portal_mis_pagos, name='portal_mis_pagos'),
    path('portal/mis-pagos/<int:pago_id>/', portal_views.portal_detalle_pago, name='portal_detalle_pago'),
    path('portal/mis-pagos/<int:pago_id>/modal/', portal_views.portal_detalle_pago_modal, name='portal_detalle_pago_modal'),
    path('portal/mis-servicios/', portal_views.portal_mis_servicios, name='portal_mis_servicios'),
    path('portal/perfil/', portal_views.portal_perfil, name='portal_perfil'),
    path('portal/cambiar-password/', portal_views.portal_cambiar_password, name='portal_cambiar_password'),
]


