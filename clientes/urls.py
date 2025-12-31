from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='cliente_list'),
    path('nuevo/', views.cliente_create, name='cliente_create'),
    path('<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('<int:pk>/editar/', views.cliente_update, name='cliente_update'),
    path('<int:pk>/eliminar/', views.cliente_delete, name='cliente_delete'),
    
    # API para autocompletado
    path('api/buscar-por-codigo-postal/', views.buscar_por_codigo_postal, name='api_buscar_por_codigo_postal'),
]


