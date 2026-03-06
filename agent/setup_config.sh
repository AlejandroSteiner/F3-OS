#!/bin/bash
# Script interactivo para configurar el agente

cd "$(dirname "$0")"

echo "🔧 Configuración del Agente Gobernante F3-OS"
echo "============================================"
echo ""

# Verificar que existe el archivo de ejemplo
if [ ! -f config/config.example.yaml ]; then
    echo "❌ Error: config/config.example.yaml no encontrado"
    exit 1
fi

# Copiar ejemplo si no existe config.yaml
if [ ! -f config/config.yaml ]; then
    echo "📋 Creando archivo de configuración desde ejemplo..."
    cp config/config.example.yaml config/config.yaml
    echo "✅ Archivo creado: config/config.yaml"
    echo ""
fi

# Leer configuración actual
CURRENT_TOKEN=$(grep -A 1 "token:" config/config.yaml | grep -v "token:" | tr -d ' "')

if [ -n "$CURRENT_TOKEN" ] && [ "$CURRENT_TOKEN" != "your_github_token_here" ]; then
    echo "✅ Token de GitHub ya configurado"
    echo ""
    read -p "¿Deseas cambiarlo? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "✅ Configuración mantenida"
        exit 0
    fi
fi

echo "📝 Configuración del Token de GitHub"
echo ""
echo "Para obtener un token de GitHub:"
echo "1. Ve a: https://github.com/settings/tokens"
echo "2. Click en 'Generate new token (classic)'"
echo "3. Selecciona los permisos:"
echo "   - repo (acceso completo a repositorios)"
echo "   - pull_requests (leer y escribir PRs)"
echo "   - issues (leer Issues)"
echo "4. Genera el token y cópialo"
echo ""
read -p "Pega tu token de GitHub aquí: " GITHUB_TOKEN

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Token vacío. Configuración cancelada."
    exit 1
fi

# Actualizar configuración
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/token:.*/token: \"$GITHUB_TOKEN\"/" config/config.yaml
else
    # Linux
    sed -i "s/token:.*/token: \"$GITHUB_TOKEN\"/" config/config.yaml
fi

echo ""
echo "✅ Token configurado correctamente"
echo ""
echo "📋 Verificando configuración..."

# Verificar que el token funciona
cd "$(dirname "$0")"
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 -c "
import yaml
from github import Github

try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    token = config.get('github', {}).get('token', '')
    if not token or token == 'your_github_token_here':
        print('❌ Token no configurado correctamente')
        exit(1)
    
    # Probar conexión
    g = Github(token)
    user = g.get_user()
    print(f'✅ Token válido. Conectado como: {user.login}')
    
except Exception as e:
    print(f'❌ Error verificando token: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Configuración completada exitosamente"
    echo ""
    echo "Ahora puedes usar el agente:"
    echo "  ./run.sh monitor"
    echo "  ./run.sh evaluate-pr --pr 1"
    echo "  ./run.sh cycle"
else
    echo ""
    echo "⚠️  El token podría no ser válido. Verifica:"
    echo "  - Que el token tenga los permisos correctos"
    echo "  - Que no haya expirado"
    echo "  - Que esté copiado correctamente"
fi







