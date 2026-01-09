#!/bin/bash
# Script para iniciar ngrok, obtener la URL y actualizar .env

echo "🚀 Iniciando ngrok y configurando SITE_URL"
echo "=" | head -c 60
echo ""

# Buscar ngrok
NGROK_CMD=""
if command -v ngrok &> /dev/null; then
    NGROK_CMD="ngrok"
elif [ -f "/snap/bin/ngrok" ]; then
    NGROK_CMD="/snap/bin/ngrok"
elif [ -f "/usr/local/bin/ngrok" ]; then
    NGROK_CMD="/usr/local/bin/ngrok"
else
    echo "❌ ngrok no encontrado"
    exit 1
fi

# Verificar configuración
if ! $NGROK_CMD config check &> /dev/null; then
    echo "⚠️  ngrok no está configurado correctamente"
    echo "Ejecuta: ./corregir_ngrok_auth.sh"
    exit 1
fi

# Obtener puerto (por defecto 8082)
PUERTO=${1:-8082}

echo "📡 Iniciando ngrok en puerto $PUERTO..."
echo ""

# Detener ngrok si ya está corriendo
pkill -f "ngrok http" 2>/dev/null
sleep 2

# Iniciar ngrok en segundo plano con opciones para evitar la página de advertencia
# --request-header-add: Agrega header para evitar la página de advertencia de ngrok
# --host-header: Reescribe el header Host para que Django funcione correctamente
$NGROK_CMD http $PUERTO \
    --request-header-add="ngrok-skip-browser-warning:true" \
    --host-header="localhost:$PUERTO" > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!
sleep 4

# Obtener la URL de ngrok
echo "Obteniendo URL de ngrok..."
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null | grep -o '"public_url":"https://[^"]*"' | head -1 | sed 's/"public_url":"//;s/"//')

if [ -z "$NGROK_URL" ]; then
    echo "❌ No se pudo obtener la URL de ngrok"
    echo "Verifica que ngrok se haya iniciado correctamente"
    kill $NGROK_PID 2>/dev/null
    exit 1
fi

echo "✅ ngrok iniciado!"
echo ""
echo "🔗 URL de ngrok: $NGROK_URL"
echo ""

# Actualizar .env
if [ -f .env ]; then
    # Backup
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null
    
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
echo "📋 Información:"
echo "  - URL de ngrok: $NGROK_URL"
echo "  - Puerto local: $PUERTO"
echo "  - ngrok PID: $NGROK_PID"
echo "  - Dashboard: http://localhost:4040"
echo ""
echo "🔄 Próximos pasos:"
echo "  1. Reinicia tu servidor Django"
echo "  2. La página de advertencia de ngrok está deshabilitada automáticamente"
echo "  3. Prueba un pago - debería redirigir sin mostrar la advertencia"
echo ""
echo "🛑 Para detener ngrok:"
echo "  kill $NGROK_PID"
echo "  o: pkill -f 'ngrok http'"
echo ""

