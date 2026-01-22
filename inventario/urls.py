from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Materiales
    path('', views.material_list, name='material_list'),
    path('materiales/nuevo/', views.material_create, name='material_create'),
    path('materiales/<int:pk>/', views.material_detail, name='material_detail'),
    path('materiales/<int:pk>/editar/', views.material_update, name='material_update'),
    path('materiales/<int:pk>/eliminar/', views.material_delete, name='material_delete'),
    
    # Categorías de materiales
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/nueva/', views.categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.categoria_update, name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
    
    # Movimientos de inventario
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/<int:pk>/', views.movimiento_detail, name='movimiento_detail'),
    path('movimientos/<int:pk>/eliminar/', views.movimiento_delete, name='movimiento_delete'),
    
    # API
    path('api/buscar-categorias/', views.api_buscar_categorias, name='api_buscar_categorias'),
    path('api/buscar-materiales/', views.api_buscar_materiales, name='api_buscar_materiales'),
]



