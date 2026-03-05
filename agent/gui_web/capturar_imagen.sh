#!/bin/bash
# Script para capturar solo la ventana del navegador con la interfaz F3-OS

echo "📸 Captura de la Interfaz F3-OS Assistant"
echo "=========================================="
echo ""
echo "Este script capturará SOLO la ventana del navegador."
echo ""
echo "Asegúrate de que:"
echo "1. El servidor GUI esté corriendo (cd agent && ./run.sh gui-server)"
echo "2. La interfaz esté abierta en http://localhost:8080"
echo "3. La ventana del navegador esté visible"
echo ""
read -p "Presiona Enter cuando estés listo para capturar..."

# Cambiar al directorio del proyecto
cd "$(dirname "$0")/../.."

# Capturar área seleccionada (más preciso)
echo ""
echo "🔍 Selecciona el área de la interfaz con el mouse..."
gnome-screenshot -a -f agent/gui_web/screenshot.png

if [ -f "agent/gui_web/screenshot.png" ]; then
    echo ""
    echo "✅ Captura guardada en: agent/gui_web/screenshot.png"
    echo ""
    read -p "¿Agregar al repositorio y subir a GitHub? (s/n): " respuesta
    
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        git add agent/gui_web/screenshot.png
        git commit -m "docs: agregar captura correcta de la interfaz GUI (solo ventana del navegador)"
        git push origin main
        echo ""
        echo "✅ Imagen agregada y subida a GitHub"
    else
        echo "Imagen guardada localmente. Puedes agregarla después con:"
        echo "  git add agent/gui_web/screenshot.png"
        echo "  git commit -m 'docs: agregar captura de la interfaz GUI'"
        echo "  git push origin main"
    fi
else
    echo "❌ Error: No se pudo capturar la imagen"
    exit 1
fi






