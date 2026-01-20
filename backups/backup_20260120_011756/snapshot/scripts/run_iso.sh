#!/bin/bash
# Script para ejecutar F3-OS desde ISO

cd "$(dirname "$0")"

if [ ! -f f3os.iso ]; then
    echo "❌ Error: f3os.iso no encontrada."
    echo "Crea la ISO primero con:"
    echo "  ./create_grub_iso.sh   (usa GRUB, más simple)"
    echo "  ./create_iso.sh        (usa Limine, si está disponible)"
    exit 1
fi

echo "=== Iniciando F3-OS desde ISO ==="
echo ""
echo "Controles:"
echo "  - Ctrl+Alt+G : Capturar/Liberar cursor"
echo "  - Ctrl+Alt+Q : Cerrar QEMU"
echo ""

qemu-system-x86_64 \
  -cdrom f3os.iso \
  -display gtk \
  -m 256M \
  -no-reboot \
  -name "F3-OS" \
  "$@"

