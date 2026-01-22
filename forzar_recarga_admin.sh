#!/bin/bash
# Script para forzar la recarga del admin limpiando caché

echo "=========================================="
echo "FORZANDO RECARGA DEL ADMIN"
echo "=========================================="

# Limpiar archivos .pyc
echo "1. Limpiando archivos .pyc..."
find . -name "*.pyc" -delete
echo "   ✅ Archivos .pyc eliminados"

# Limpiar directorios __pycache__
echo "2. Limpiando directorios __pycache__..."
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
echo "   ✅ Directorios __pycache__ eliminados"

# Limpiar caché de Django (si existe)
echo "3. Limpiando caché de Django..."
if [ -d "core/cache" ]; then
    rm -rf core/cache/*
    echo "   ✅ Caché de Django limpiado"
else
    echo "   ⚠️  No se encontró directorio de caché"
fi

echo ""
echo "=========================================="
echo "PASOS SIGUIENTES:"
echo "=========================================="
echo "1. Reinicia el servidor Django:"
echo "   python manage.py runserver"
echo ""
echo "2. Ve al admin:"
echo "   http://localhost:8000/admin/core/configuracionsistema/"
echo ""
echo "3. Recarga la página con Ctrl+F5"
echo "=========================================="



