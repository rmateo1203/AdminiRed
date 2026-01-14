#!/bin/bash
# Script para configurar ngrok y actualizar SITE_URL automáticamente

echo "🚀 Configurando ngrok para Mercado Pago Auto-Return"
echo "=" | head -c 60
echo ""

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok no está instalado."
    echo ""
    echo "Instalando ngrok..."
    if command -v snap &> /dev/null; then
        sudo snap install ngrok
    else
        echo "Por favor instala ngrok manualmente:"
        echo "  1. Visita: https://ngrok.com/download"
        echo "  2. O usa: sudo snap install ngrok"
        exit 1
    fi
fi

# Verificar si ngrok tiene authtoken configurado
if ! ngrok config check &> /dev/null; then
    echo "⚠️  ngrok necesita authtoken"
    echo ""
    echo "Para obtener tu authtoken:"
    echo "  1. Crea una cuenta en: https://dashboard.ngrok.com/signup"
    echo "  2. Obtén tu authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "  3. Ejecuta: ngrok config add-authtoken TU_AUTHTOKEN"
    echo ""
    read -p "¿Tienes tu authtoken? (s/n): " tiene_token
    
    if [ "$tiene_token" != "s" ] && [ "$tiene_token" != "S" ]; then
        echo "Por favor configura ngrok primero y luego ejecuta este script nuevamente."
        exit 1
    fi
    
    read -p "Ingresa tu authtoken de ngrok: " authtoken
    ngrok config add-authtoken "$authtoken"
    echo "✅ Authtoken configurado"
fi

# Detener ngrok si está corriendo
pkill -f "ngrok http" 2>/dev/null
sleep 1

# Iniciar ngrok en segundo plano
echo "Iniciando ngrok..."
ngrok http 8000 > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
sleep 3

# Obtener la URL de ngrok desde la API local
echo "Obteniendo URL de ngrok..."
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*"' | head -1 | sed 's/"public_url":"//;s/"//')

if [ -z "$NGROK_URL" ]; then
    echo "❌ No se pudo obtener la URL de ngrok"
    echo "Verifica que ngrok esté corriendo: ngrok http 8000"
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo "✅ ngrok iniciado: $NGROK_URL"

# Actualizar .env
if [ -f .env ]; then
    # Backup del .env
    cp .env .env.backup
    echo "✅ Backup creado: .env.backup"
    
    # Actualizar SITE_URL
    if grep -q "^SITE_URL=" .env; then
        sed -i "s|^SITE_URL=.*|SITE_URL=$NGROK_URL|" .env
        echo "✅ .env actualizado: SITE_URL=$NGROK_URL"
    else
        echo "SITE_URL=$NGROK_URL" >> .env
        echo "✅ SITE_URL agregado a .env: $NGROK_URL"
    fi
else
    echo "⚠️  Archivo .env no encontrado. Creándolo..."
    echo "SITE_URL=$NGROK_URL" > .env
    echo "✅ .env creado con SITE_URL=$NGROK_URL"
fi

echo ""
echo "=" | head -c 60
echo ""
echo "✅ Configuración completada!"
echo ""
echo "📋 Información importante:"
echo "  - URL de ngrok: $NGROK_URL"
echo "  - ngrok está corriendo en segundo plano (PID: $NGROK_PID)"
echo "  - Para detener ngrok: kill $NGROK_PID"
echo ""
echo "🔄 Próximos pasos:"
echo "  1. Reinicia tu servidor Django"
echo "  2. Verifica en los logs que ya no aparezca el mensaje de advertencia"
echo "  3. Prueba un pago - debería redirigir automáticamente"
echo ""
echo "💡 Nota: La URL de ngrok cambiará cada vez que reinicies ngrok"
echo "         (a menos que uses un dominio reservado de ngrok)"




