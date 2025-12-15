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
]

