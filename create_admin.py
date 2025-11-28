#!/usr/bin/env python
"""
Script para crear un superusuario de forma no interactiva.
Uso: python create_admin.py
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Crea un superusuario si no existe."""
    username = input('Nombre de usuario: ').strip()
    email = input('Correo electrónico (opcional): ').strip() or ''
    
    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        print(f'❌ El usuario "{username}" ya existe.')
        return
    
    # Solicitar contraseña
    while True:
        password = input('Contraseña: ').strip()
        if len(password) < 8:
            print('⚠️  La contraseña debe tener al menos 8 caracteres.')
            continue
        password_confirm = input('Confirmar contraseña: ').strip()
        if password != password_confirm:
            print('❌ Las contraseñas no coinciden. Intenta de nuevo.')
            continue
        break
    
    # Crear el superusuario
    try:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f'✅ Superusuario "{username}" creado exitosamente!')
        print(f'   Puedes iniciar sesión en: http://127.0.0.1:8000/admin/')
    except Exception as e:
        print(f'❌ Error al crear el superusuario: {e}')

if __name__ == '__main__':
    print('=' * 50)
    print('Creación de Superusuario - AdminiRed')
    print('=' * 50)
    create_superuser()

