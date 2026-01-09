#!/bin/bash
# Script para corregir el authtoken de ngrok

echo "🔧 Corrector de Authtoken de ngrok"
echo "=" | head -c 50
echo ""

# Verificar si ngrok está instalado
NGROK_CMD=""

# Buscar ngrok en diferentes ubicaciones
if command -v ngrok &> /dev/null; then
    NGROK_CMD="ngrok"
elif [ -f "/snap/bin/ngrok" ]; then
    NGROK_CMD="/snap/bin/ngrok"
elif [ -f "/usr/local/bin/ngrok" ]; then
    NGROK_CMD="/usr/local/bin/ngrok"
elif [ -f "$HOME/.local/bin/ngrok" ]; then
    NGROK_CMD="$HOME/.local/bin/ngrok"
else
    echo "❌ ngrok no está instalado o no se encuentra en el PATH"
    echo ""
    echo "Ubicaciones verificadas:"
    echo "  - /snap/bin/ngrok"
    echo "  - /usr/local/bin/ngrok"
    echo "  - ~/.local/bin/ngrok"
    echo ""
    echo "Instala con: sudo snap install ngrok"
    echo "O agrega ngrok al PATH si ya está instalado"
    exit 1
fi

echo "✅ ngrok encontrado en: $NGROK_CMD"

echo ""
echo "El token que tienes configurado parece ser inválido."
echo ""
echo "Para corregir esto:"
echo ""
echo "1. Ve a: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "2. Inicia sesión (o crea una cuenta si no tienes)"
echo "3. Copia tu authtoken completo (debe ser largo, ~40 caracteres)"
echo ""
read -p "¿Ya tienes tu authtoken? (s/n): " tiene_token

if [ "$tiene_token" != "s" ] && [ "$tiene_token" != "S" ]; then
    echo ""
    echo "Por favor:"
    echo "  1. Visita: https://dashboard.ngrok.com/signup"
    echo "  2. Crea una cuenta (es gratis)"
    echo "  3. Ve a: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "  4. Copia tu authtoken"
    echo "  5. Ejecuta este script nuevamente"
    exit 1
fi

echo ""
read -p "Pega tu authtoken aquí (o presiona Enter para usar el token por defecto): " authtoken

# Si no se ingresó token, usar el token por defecto
if [ -z "$authtoken" ]; then
    authtoken="381uKw30O08GisDZWGinwuPxmz3_4ZGQQo11zWBmfMZwet2uM"
    echo "Usando token por defecto configurado."
fi

# Validar que el token tenga al menos 30 caracteres
if [ ${#authtoken} -lt 30 ]; then
    echo ""
    echo "❌ El authtoken parece muy corto. Un authtoken válido debe tener al menos 30 caracteres."
    echo "   Por favor verifica que copiaste el token completo."
    exit 1
fi

# Eliminar configuración anterior
echo ""
echo "Eliminando configuración anterior..."
rm -f ~/.config/ngrok/ngrok.yml
rm -f ~/.ngrok2/ngrok.yml

# Configurar nuevo authtoken
echo "Configurando nuevo authtoken..."
$NGROK_CMD config add-authtoken "$authtoken"

# Verificar
if $NGROK_CMD config check &> /dev/null; then
    echo ""
    echo "✅ Authtoken configurado correctamente!"
    echo ""
    echo "Ahora puedes iniciar ngrok con:"
    echo "  ngrok http 8000"
    echo ""
    echo "O si Django está en otro puerto:"
    echo "  ngrok http 8082"
else
    echo ""
    echo "❌ Error al configurar el authtoken"
    echo "Por favor verifica que el token sea correcto"
    exit 1
fi

