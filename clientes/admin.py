from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django import forms
from simple_history.admin import SimpleHistoryAdmin
from .models import Cliente


class ClienteAdminForm(forms.ModelForm):
    """Formulario personalizado para el admin de Cliente con campo de contraseña."""
    nueva_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Dejar en blanco para no cambiar'}),
        label='Nueva contraseña del portal',
        help_text='Dejar en blanco si no deseas cambiar la contraseña. Mínimo 8 caracteres.'
    )
    confirmar_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}),
        label='Confirmar contraseña'
    )
    
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        # Solo validar si se intenta cambiar la contraseña
        if nueva_password or confirmar_password:
            if not nueva_password:
                raise forms.ValidationError({'nueva_password': 'Debes ingresar una contraseña si deseas cambiarla.'})
            
            if not confirmar_password:
                raise forms.ValidationError({'confirmar_password': 'Debes confirmar la contraseña.'})
            
            if nueva_password != confirmar_password:
                raise forms.ValidationError({'confirmar_password': 'Las contraseñas no coinciden.'})
            
            if len(nueva_password) < 8:
                raise forms.ValidationError({'nueva_password': 'La contraseña debe tener al menos 8 caracteres.'})
        
        return cleaned_data


@admin.register(Cliente)
class ClienteAdmin(SimpleHistoryAdmin):
    form = ClienteAdminForm
    list_display = [
        'nombre_completo_display',
        'telefono',
        'email',
        'ciudad',
        'estado_cliente',
        'fecha_registro',
    ]
    list_filter = [
        'estado_cliente',
        'ciudad',
        'estado',
        'fecha_registro',
    ]
    search_fields = ['nombre', 'apellido1', 'apellido2', 'telefono', 'email', 'direccion']
    readonly_fields = [
        'fecha_registro',
        'fecha_actualizacion',
    ]
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre', 'apellido1', 'apellido2', 'email', 'telefono')
        }),
        ('Dirección', {
            'fields': ('direccion', 'ciudad', 'estado', 'codigo_postal')
        }),
        ('Estado', {
            'fields': ('estado_cliente',)
        }),
        ('Información Adicional', {
            'fields': ('notas',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Obtener el queryset de clientes."""
        return super().get_queryset(request)
    
    def nombre_completo_display(self, obj):
        """Muestra el nombre completo del cliente."""
        return obj.nombre_completo
    nombre_completo_display.short_description = 'Cliente'
    nombre_completo_display.admin_order_field = 'nombre'
    
    
    def save_model(self, request, obj, form, change):
        """Sobrescribe save_model para manejar cambio de contraseña si existe."""
        # Guardar el modelo primero
        super().save_model(request, obj, form, change)
        
        # Manejar cambio de contraseña si se proporcionó y el modelo tiene el método
        nueva_password = form.cleaned_data.get('nueva_password')
        if nueva_password and hasattr(obj, 'usuario') and obj.usuario:
            try:
                if hasattr(obj, 'resetear_password_portal'):
                    obj.resetear_password_portal(password=nueva_password, enviar_email=False)
                    messages.success(
                        request,
                        f'Contraseña del portal actualizada para {obj.nombre_completo}.'
                    )
            except Exception as e:
                messages.error(
                    request,
                    f'Error al cambiar la contraseña: {str(e)}'
                )
    
    actions = ['crear_usuario_portal', 'forzar_cambio_password', 'resetear_password', 'establecer_password']
    
    def crear_usuario_portal(self, request, queryset):
        """Acción para crear usuarios del portal para clientes seleccionados."""
        import secrets
        import string
        
        creados = 0
        ya_tienen = 0
        errores = 0
        
        for cliente in queryset:
            if hasattr(cliente, 'usuario') and cliente.usuario:
                ya_tienen += 1
                continue  # Ya tiene usuario
            
            try:
                # Crear usuario (generará contraseña automáticamente y enviará email)
                if hasattr(cliente, 'crear_usuario_portal'):
                    usuario = cliente.crear_usuario_portal(enviar_email=True)
                    creados += 1
                else:
                    continue
                
                # Obtener la contraseña generada (si fue generada automáticamente)
                # Nota: No podemos obtener la contraseña después de crearla por seguridad
                # El email se envió automáticamente con las credenciales
                self.message_user(
                    request,
                    f'✅ Usuario creado para {cliente.nombre_completo} ({usuario.username}). '
                    f'Las credenciales se han enviado por email a {cliente.email}',
                    level=messages.SUCCESS
                )
            except Exception as e:
                errores += 1
                self.message_user(
                    request,
                    f'❌ Error al crear usuario para {cliente.nombre_completo}: {str(e)}',
                    level=messages.ERROR
                )
        
        # Mensaje resumen
        if creados > 0:
            self.message_user(
                request,
                f'✅ {creados} usuario(s) creado(s) exitosamente. {ya_tienen} cliente(s) ya tenían usuario. {errores} error(es).',
                level=messages.SUCCESS
            )
        elif ya_tienen > 0:
            self.message_user(
                request,
                f'ℹ️ {ya_tienen} cliente(s) seleccionado(s) ya tienen usuario asignado.',
                level=messages.INFO
            )
    
    crear_usuario_portal.short_description = '🔐 Crear usuario para portal (clientes seleccionados)'
    
    def forzar_cambio_password(self, request, queryset):
        """Acción para forzar el cambio de contraseña a los clientes seleccionados."""
        if hasattr(Cliente, 'debe_cambiar_password'):
            count = queryset.update(debe_cambiar_password=True)
            self.message_user(
                request,
                f'{count} cliente(s) deberán cambiar su contraseña en el próximo inicio de sesión.',
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                'Esta funcionalidad no está disponible en este modelo.',
                messages.WARNING
            )
    forzar_cambio_password.short_description = '🔒 Forzar cambio de contraseña'
    
    def resetear_password(self, request, queryset):
        """Acción para resetear la contraseña del portal a los clientes seleccionados."""
        reseteados = 0
        clientes_sin_usuario = []
        errores = 0
        contraseñas_no_enviadas = []
        
        for cliente in queryset:
            if not hasattr(cliente, 'usuario') or not cliente.usuario:
                clientes_sin_usuario.append(cliente.nombre_completo)
                continue
            
            try:
                # Resetear contraseña (se generará automáticamente y se enviará por email)
                if hasattr(cliente, 'resetear_password_portal'):
                    nueva_password = cliente.resetear_password_portal(enviar_email=True)
                    reseteados += 1
                else:
                    continue
                
                self.message_user(
                    request,
                    f'✅ Contraseña restablecida para {cliente.nombre_completo}. '
                    f'Se ha enviado un email a {cliente.email} con la nueva contraseña.',
                    level=messages.SUCCESS
                )
            except ValueError as e:
                # Error esperado (ej: no se pudo enviar email pero se generó contraseña)
                if 'Nueva Contraseña:' in str(e):
                    reseteados += 1
                    contraseñas_no_enviadas.append((cliente.nombre_completo, str(e)))
                else:
                    errores += 1
                    self.message_user(
                        request,
                        f'❌ Error al resetear contraseña para {cliente.nombre_completo}: {str(e)}',
                        level=messages.ERROR
                    )
            except Exception as e:
                errores += 1
                self.message_user(
                    request,
                    f'❌ Error al resetear contraseña para {cliente.nombre_completo}: {str(e)}',
                    level=messages.ERROR
                )
        
        # Mostrar mensajes para clientes sin usuario
        if clientes_sin_usuario:
            if len(clientes_sin_usuario) == 1:
                self.message_user(
                    request,
                    f'⚠️ El cliente "{clientes_sin_usuario[0]}" no tiene usuario del portal. '
                    f'Crea un usuario primero usando la acción "🔐 Crear usuario para portal".',
                    level=messages.WARNING
                )
            else:
                nombres = ', '.join(clientes_sin_usuario[:5])  # Mostrar máximo 5 nombres
                if len(clientes_sin_usuario) > 5:
                    nombres += f' y {len(clientes_sin_usuario) - 5} más'
                self.message_user(
                    request,
                    f'⚠️ {len(clientes_sin_usuario)} cliente(s) no tienen usuario del portal: {nombres}. '
                    f'Crea usuarios primero usando la acción "🔐 Crear usuario para portal".',
                    level=messages.WARNING
                )
        
        # Mensaje resumen
        if reseteados > 0:
            mensaje = f'✅ {reseteados} contraseña(s) restablecida(s) exitosamente.'
            if contraseñas_no_enviadas:
                mensaje += f' {len(contraseñas_no_enviadas)} contraseña(s) no se pudieron enviar por email (ver detalles arriba).'
            if errores > 0:
                mensaje += f' {errores} error(es).'
            self.message_user(request, mensaje, level=messages.SUCCESS)
        elif not clientes_sin_usuario and errores == 0:
            # Caso especial: no se procesó ningún cliente (no debería pasar, pero por seguridad)
            self.message_user(
                request,
                'ℹ️ No se procesó ningún cliente. Verifica que los clientes seleccionados tengan usuario del portal.',
                level=messages.INFO
            )
    
    resetear_password.short_description = '🔑 Restablecer contraseña del portal'
    
    def establecer_password(self, request, queryset):
        """Acción para establecer manualmente la contraseña del portal a los clientes seleccionados."""
        # Si se envió el formulario con la contraseña
        if 'aplicar_password' in request.POST:
            password = request.POST.get('nueva_password', '').strip()
            confirmar_password = request.POST.get('confirmar_password', '').strip()
            
            if not password:
                self.message_user(request, '❌ La contraseña no puede estar vacía.', level=messages.ERROR)
                return
            
            if password != confirmar_password:
                self.message_user(request, '❌ Las contraseñas no coinciden.', level=messages.ERROR)
                return
            
            if len(password) < 8:
                self.message_user(request, '❌ La contraseña debe tener al menos 8 caracteres.', level=messages.ERROR)
                return
            
            establecidas = 0
            clientes_sin_usuario = []
            errores = 0
            
            # Obtener los IDs de los clientes seleccionados
            cliente_ids = request.POST.getlist('_selected_action')
            clientes_seleccionados = queryset.filter(id__in=cliente_ids)
            
            for cliente in clientes_seleccionados:
                if not hasattr(cliente, 'usuario') or not cliente.usuario:
                    clientes_sin_usuario.append(cliente.nombre_completo)
                    continue
                
                try:
                    if hasattr(cliente, 'resetear_password_portal'):
                        cliente.resetear_password_portal(password=password, enviar_email=False)
                        establecidas += 1
                    else:
                        continue
                    self.message_user(
                        request,
                        f'✅ Contraseña establecida para {cliente.nombre_completo} (Usuario: {cliente.usuario.username}).',
                        level=messages.SUCCESS
                    )
                except Exception as e:
                    errores += 1
                    self.message_user(
                        request,
                        f'❌ Error al establecer contraseña para {cliente.nombre_completo}: {str(e)}',
                        level=messages.ERROR
                    )
            
            # Mensaje resumen
            if establecidas > 0:
                mensaje = f'✅ {establecidas} contraseña(s) establecida(s) exitosamente.'
                if clientes_sin_usuario:
                    mensaje += f' {len(clientes_sin_usuario)} cliente(s) no tienen usuario del portal.'
                if errores > 0:
                    mensaje += f' {errores} error(es).'
                self.message_user(request, mensaje, level=messages.SUCCESS)
            elif clientes_sin_usuario:
                self.message_user(
                    request,
                    f'⚠️ Los clientes seleccionados no tienen usuario del portal. Crea usuarios primero.',
                    level=messages.WARNING
                )
            
            return
        
        # Si no se envió el formulario, mostrar la página de confirmación
        if queryset.count() == 1:
            cliente = queryset.first()
            if not hasattr(cliente, 'usuario') or not cliente.usuario:
                self.message_user(
                    request,
                    f'⚠️ El cliente "{cliente.nombre_completo}" no tiene usuario del portal. '
                    f'Crea un usuario primero usando la acción "🔐 Crear usuario para portal".',
                    level=messages.WARNING
                )
                return
        
        # Renderizar template con formulario
        from django.template.response import TemplateResponse
        
        context = {
            'title': 'Establecer contraseña manualmente',
            'clientes': queryset,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        
        return TemplateResponse(request, 'admin/clientes/cliente/establecer_password.html', context)
    
    establecer_password.short_description = '✏️ Establecer contraseña manualmente'
