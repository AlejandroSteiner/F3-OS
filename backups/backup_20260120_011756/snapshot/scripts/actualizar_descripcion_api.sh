#!/bin/bash
# Script para actualizar la descripción del repositorio usando la API de GitHub con curl

REPO_OWNER="AlejandroSteiner"
REPO_NAME="F3-OS"

# Descripción corta (máximo 160 caracteres)
SHORT_DESCRIPTION="F3-OS: Sistema operativo experimental de código abierto con modelo innovador de 3 hilos (CPU/RAM/MEM) fusionados en un embudo adaptativo. Ciclo: Lógico → Ilógico → Síntesis → Perfecto."

# Topics como array JSON
TOPICS_JSON="[\"rust\",\"operating-system\",\"kernel\",\"osdev\",\"bare-metal\",\"multiboot\",\"x86-64\",\"experimental\",\"open-source\",\"systems-programming\",\"f3-os\",\"embedded\",\"no-std\",\"qemu\",\"grub\"]"

echo "=== Actualizar Descripción del Repositorio en GitHub ==="
echo ""
echo "📝 Descripción: $SHORT_DESCRIPTION"
echo "🏷️  Topics: rust, operating-system, kernel, osdev, bare-metal, multiboot, x86-64, experimental, open-source, systems-programming, f3-os, embedded, no-std, qemu, grub"
echo ""

# Intentar obtener token de varias fuentes
GITHUB_TOKEN=""

# 1. De variable de entorno
if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ Token encontrado en variable de entorno"
# 2. De git credential helper (si está configurado)
elif git credential fill <<< "protocol=https
host=github.com
" 2>/dev/null | grep password | cut -d= -f2 | head -1 | grep -q .; then
    GITHUB_TOKEN=$(git credential fill <<< "protocol=https
host=github.com
" 2>/dev/null | grep password | cut -d= -f2 | head -1)
    echo "✅ Token encontrado en git credentials"
fi

# Si no hay token, pedir al usuario
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  No se encontró token de GitHub"
    echo ""
    echo "Para actualizar el repositorio, necesitas un Personal Access Token (PAT):"
    echo ""
    echo "1. Crea un token en: https://github.com/settings/tokens"
    echo "   - Selecciona 'repo' scope"
    echo "   - Copia el token generado"
    echo ""
    read -sp "Ingresa tu GitHub Personal Access Token (o presiona Enter para cancelar): " GITHUB_TOKEN
    echo ""
    
    if [ -z "$GITHUB_TOKEN" ]; then
        echo ""
        echo "❌ Operación cancelada"
        echo ""
        echo "Alternativa: Actualiza manualmente en:"
        echo "https://github.com/$REPO_OWNER/$REPO_NAME/settings"
        exit 0
    fi
fi

echo ""
echo "🔄 Actualizando repositorio..."

# Actualizar descripción y topics
RESPONSE=$(curl -s -w "\n%{http_code}" -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME" \
  -d "{
    \"description\": \"$SHORT_DESCRIPTION\",
    \"homepage\": \"\",
    \"topics\": $TOPICS_JSON
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Repositorio actualizado exitosamente!"
    echo ""
    echo "Verifica en: https://github.com/$REPO_OWNER/$REPO_NAME"
    echo ""
    echo "La descripción y topics han sido actualizados."
else
    echo "❌ Error al actualizar repositorio"
    echo "   HTTP Code: $HTTP_CODE"
    echo "   Respuesta: $BODY"
    echo ""
    echo "Posibles causas:"
    echo "  - Token inválido o expirado"
    echo "  - Token no tiene permisos 'repo'"
    echo "  - Problemas de conexión"
    echo ""
    echo "Intenta:"
    echo "  1. Verificar el token en https://github.com/settings/tokens"
    echo "  2. Asegurarte de que tiene permisos 'repo'"
    echo "  3. Actualizar manualmente en https://github.com/$REPO_OWNER/$REPO_NAME/settings"
fi
