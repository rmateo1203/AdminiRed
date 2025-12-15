from django.urls import path
from . import views

app_name = 'notificaciones'

urlpatterns = [
    path('', views.notificacion_list, name='notificacion_list'),
    path('nueva/', views.notificacion_create, name='notificacion_create'),
    path('nueva/cliente/<int:cliente_id>/', views.notificacion_create, name='notificacion_create_for_cliente'),
    path('<int:pk>/', views.notificacion_detail, name='notificacion_detail'),
    path('<int:pk>/editar/', views.notificacion_update, name='notificacion_update'),
    path('<int:pk>/eliminar/', views.notificacion_delete, name='notificacion_delete'),
    path('<int:pk>/enviar/', views.notificacion_send, name='notificacion_send'),
]

