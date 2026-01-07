from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Instalacion, MaterialInstalacion
from inventario.models import Material


@login_required
def gestionar_materiales(request, instalacion_id):
    """Gestiona los materiales de una instalación."""
    instalacion = get_object_or_404(Instalacion, pk=instalacion_id)
    materiales_instalacion = MaterialInstalacion.objects.filter(instalacion=instalacion).select_related('material')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'agregar':
            material_id = request.POST.get('material_id')
            cantidad = request.POST.get('cantidad', '0')
            notas = request.POST.get('notas', '')
            
            try:
                material = Material.objects.get(pk=material_id)
                cantidad = int(cantidad)
                
                if cantidad <= 0:
                    messages.error(request, 'La cantidad debe ser mayor a 0.')
                    return redirect('instalaciones:gestionar_materiales', instalacion_id=instalacion_id)
                
                # Verificar stock
                if material.stock_actual < cantidad:
                    messages.warning(request, f'Stock insuficiente. Disponible: {material.stock_actual}, Necesario: {cantidad}')
                    return redirect('instalaciones:gestionar_materiales', instalacion_id=instalacion_id)
                
                # Crear o actualizar material de instalación
                material_inst, created = MaterialInstalacion.objects.get_or_create(
                    instalacion=instalacion,
                    material=material,
                    defaults={'cantidad': cantidad, 'notas': notas}
                )
                
                if not created:
                    material_inst.cantidad = cantidad
                    material_inst.notas = notas
                    material_inst.save()
                    messages.success(request, f'Material "{material.nombre}" actualizado exitosamente.')
                else:
                    messages.success(request, f'Material "{material.nombre}" agregado exitosamente.')
                
            except Material.DoesNotExist:
                messages.error(request, 'Material no encontrado.')
            except ValueError:
                messages.error(request, 'Cantidad inválida.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        
        elif accion == 'eliminar':
            material_inst_id = request.POST.get('material_inst_id')
            try:
                material_inst = MaterialInstalacion.objects.get(pk=material_inst_id, instalacion=instalacion)
                material_nombre = material_inst.material.nombre
                material_inst.delete()
                messages.success(request, f'Material "{material_nombre}" eliminado exitosamente.')
            except MaterialInstalacion.DoesNotExist:
                messages.error(request, 'Material de instalación no encontrado.')
        
        return redirect('instalaciones:gestionar_materiales', instalacion_id=instalacion_id)
    
    # Obtener materiales disponibles
    materiales_disponibles = Material.objects.filter(
        estado__in=['disponible', 'bajo_stock']
    ).order_by('nombre')
    
    # Verificar disponibilidad
    materiales_insuficientes = []
    for mat_inst in materiales_instalacion:
        if mat_inst.material.stock_actual < mat_inst.cantidad:
            materiales_insuficientes.append({
                'material': mat_inst.material,
                'necesario': mat_inst.cantidad,
                'disponible': mat_inst.material.stock_actual,
                'faltante': mat_inst.cantidad - mat_inst.material.stock_actual
            })
    
    context = {
        'instalacion': instalacion,
        'materiales_instalacion': materiales_instalacion,
        'materiales_disponibles': materiales_disponibles,
        'materiales_insuficientes': materiales_insuficientes,
    }
    
    return render(request, 'instalaciones/gestionar_materiales.html', context)


@login_required
def get_material_info(request, material_id):
    """API para obtener información de un material."""
    try:
        material = get_object_or_404(Material, pk=material_id)
        return JsonResponse({
            'success': True,
            'nombre': material.nombre,
            'stock_actual': material.stock_actual,
            'stock_minimo': material.stock_minimo,
            'unidad_medida': material.unidad_medida,
            'unidad_medida_display': material.get_unidad_medida_display(),
            'estado': material.estado,
            'estado_display': material.get_estado_display(),
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


