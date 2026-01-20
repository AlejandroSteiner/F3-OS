#!/bin/bash
# Script para actualizar la descripción del repositorio en GitHub usando la API

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== Configurar Descripción del Repositorio en GitHub ==="
echo ""

REPO_OWNER="AlejandroSteiner"
REPO_NAME="F3-OS"

# Descripción corta (máximo 160 caracteres)
SHORT_DESCRIPTION="F3-OS: Sistema operativo experimental de código abierto con modelo innovador de 3 hilos (CPU/RAM/MEM) fusionados en un embudo adaptativo. Ciclo: Lógico → Ilógico → Síntesis → Perfecto."

# Descripción completa
FULL_DESCRIPTION="Sistema operativo experimental de código abierto escrito en Rust que implementa un modelo innovador de gestión de recursos basado en 3 hilos fundamentales (CPU, RAM, MEM) que se fusionan en un embudo central (F3 Core), creando un ciclo adaptativo de retroalimentación."

# Topics
TOPICS=(
    "rust"
    "operating-system"
    "kernel"
    "osdev"
    "bare-metal"
    "multiboot"
    "x86-64"
    "experimental"
    "open-source"
    "systems-programming"
    "f3-os"
    "embedded"
    "no-std"
    "qemu"
    "grub"
)

# Homepage (opcional)
HOMEPAGE=""

echo "📝 Descripción corta:"
echo "   $SHORT_DESCRIPTION"
echo ""
echo "📄 Descripción completa:"
echo "   $FULL_DESCRIPTION"
echo ""
echo "🏷️  Topics:"
echo "   ${TOPICS[*]}"
echo ""

# Verificar si gh CLI está instalado
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI encontrado"
    echo ""
    read -p "¿Deseas actualizar el repositorio con esta descripción? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[SsYy]$ ]]; then
        echo ""
        echo "🔄 Actualizando repositorio..."
        
        # Actualizar descripción
        gh repo edit "$REPO_OWNER/$REPO_NAME" \
            --description "$SHORT_DESCRIPTION" \
            --homepage "$HOMEPAGE" || {
            echo "❌ Error: No se pudo actualizar la descripción"
            echo "   Verifica que tienes permisos y que gh está autenticado:"
            echo "   gh auth login"
            exit 1
        }
        
        # Actualizar topics
        gh repo edit "$REPO_OWNER/$REPO_NAME" \
            --add-topic "${TOPICS[@]}" || {
            echo "⚠️  No se pudieron actualizar los topics"
        }
        
        echo ""
        echo "✅ Repositorio actualizado exitosamente"
        echo ""
        echo "Verifica en: https://github.com/$REPO_OWNER/$REPO_NAME"
    else
        echo ""
        echo "⏭️  Operación cancelada"
        echo ""
        echo "Para actualizar manualmente:"
        echo "1. Ve a https://github.com/$REPO_OWNER/$REPO_NAME/settings"
        echo "2. Actualiza la descripción y topics en la sección 'General'"
    fi
else
    echo "⚠️  GitHub CLI (gh) no está instalado"
    echo ""
    echo "Opciones:"
    echo ""
    echo "1. Instalar GitHub CLI:"
    echo "   curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg"
    echo "   sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg"
    echo "   echo \"deb [arch=\$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main\" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null"
    echo "   sudo apt update && sudo apt install gh"
    echo ""
    echo "2. Actualizar manualmente desde la web:"
    echo "   Ve a https://github.com/$REPO_OWNER/$REPO_NAME/settings"
    echo "   Actualiza la descripción en la sección 'General'"
    echo ""
    echo "3. Usar la API de GitHub directamente:"
    echo "   Ver instrucciones en DESCRIPCION_REPO.md"
fi
