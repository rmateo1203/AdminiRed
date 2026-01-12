#!/usr/bin/env python
"""
Script para crear usuarios del portal para clientes que no tienen usuario.
Uso: python crear_usuarios_clientes.py
"""
import os
import sys
import django
import secrets
import string

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminired.settings')
django.setup()

from clientes.models import Cliente


def generar_contraseña():
    """Genera una contraseña aleatoria segura."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))


def crear_usuarios_clientes():
    """Crea usuarios para clientes que no tienen usuario."""
    print("=" * 70)
    print("🔐 CREACIÓN DE USUARIOS PARA PORTAL DE CLIENTES")
    print("=" * 70)
    print()
    
    # Obtener clientes sin usuario
    clientes_sin_usuario = Cliente.objects.filter(
        usuario__isnull=True,
        is_deleted=False
    )
    
    total = clientes_sin_usuario.count()
    
    if total == 0:
        print("✅ Todos los clientes activos ya tienen usuario asignado.")
        return
    
    print(f"📊 Encontrados {total} cliente(s) sin usuario")
    print()
    
    # Preguntar confirmación
    respuesta = input(f"¿Deseas crear usuarios para estos {total} cliente(s)? (s/n): ").strip().lower()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("❌ Operación cancelada.")
        return
    
    print()
    print("Creando usuarios...")
    print("-" * 70)
    
    creados = 0
    errores = 0
    credenciales = []
    
    for cliente in clientes_sin_usuario:
        try:
            password = generar_contraseña()
            usuario = cliente.crear_usuario_portal(password=password)
            creados += 1
            
            credenciales.append({
                'cliente': cliente.nombre_completo,
                'email': cliente.email or 'N/A',
                'telefono': cliente.telefono,
                'username': usuario.username,
                'password': password
            })
            
            print(f"✅ {cliente.nombre_completo}")
            print(f"   Username: {usuario.username}")
            print(f"   Contraseña: {password}")
            print()
            
        except Exception as e:
            errores += 1
            print(f"❌ Error con {cliente.nombre_completo}: {str(e)}")
            print()
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"✅ Usuarios creados: {creados}")
    print(f"❌ Errores: {errores}")
    print()
    
    # Guardar credenciales en archivo
    if credenciales:
        filename = 'credenciales_clientes.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("CREDENCIALES DE ACCESO AL PORTAL\n")
            f.write("=" * 70 + "\n\n")
            
            for cred in credenciales:
                f.write(f"Cliente: {cred['cliente']}\n")
                f.write(f"Email: {cred['email']}\n")
                f.write(f"Teléfono: {cred['telefono']}\n")
                f.write(f"Username: {cred['username']}\n")
                f.write(f"Contraseña: {cred['password']}\n")
                f.write("-" * 70 + "\n\n")
        
        print(f"💾 Credenciales guardadas en: {filename}")
        print("⚠️  IMPORTANTE: Envía estas credenciales a los clientes de forma segura.")
        print()


if __name__ == '__main__':
    crear_usuarios_clientes()






