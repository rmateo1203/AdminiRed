#!/bin/bash
# Script para iniciar ngrok fácilmente

echo "🚀 Iniciador de ngrok"
echo "=" | head -c 50
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

echo "✅ Iniciando ngrok en puerto $PUERTO..."
echo ""
echo "🔗 ngrok estará disponible en: http://localhost:4040"
echo "🛑 Presiona Ctrl+C para detener"
echo ""

# Iniciar ngrok
$NGROK_CMD http $PUERTO


