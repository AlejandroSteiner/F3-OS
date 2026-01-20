#!/bin/bash
# Script para ejecutar F3-OS en QEMU de forma segura

cd "$(dirname "$0")"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== F3-OS Launcher ===${NC}"
echo ""

# Verificar que kernel.bin existe
if [ ! -f kernel.bin ]; then
    echo -e "${RED}❌ Error: kernel.bin no encontrado.${NC}"
    echo "Ejecuta primero: ./build.sh"
    exit 1
fi

# Verificar que QEMU está instalado
if ! command -v qemu-system-x86_64 &> /dev/null; then
    echo -e "${RED}❌ Error: qemu-system-x86_64 no encontrado.${NC}"
    echo "Instala con: sudo apt install -y qemu-system-x86"
    exit 1
fi

echo -e "${YELLOW}Iniciando F3-OS en QEMU...${NC}"
echo ""
echo "Controles:"
echo "  - Ctrl+Alt+G : Capturar/Liberar cursor"
echo "  - Ctrl+Alt+Q : Cerrar QEMU"
echo "  - Ctrl+Alt+2 : Monitor de QEMU"
echo "  - Ctrl+Alt+1 : Volver a la pantalla principal"
echo ""
echo -e "${GREEN}Iniciando...${NC}"
echo ""

# Ejecutar QEMU con multiboot
# Usar -kernel para cargar directamente (requiere Multiboot header)
# Si no funciona, intenta crear ISO con Limine
qemu-system-x86_64 \
  -kernel kernel.bin \
  -display gtk \
  -m 256M \
  -no-reboot \
  -machine type=pc \
  -cpu qemu64 \
  -boot order=c \
  -no-shutdown \
  -serial stdio \
  -name "F3-OS" \
  "$@"

echo ""
echo -e "${GREEN}QEMU cerrado.${NC}"

