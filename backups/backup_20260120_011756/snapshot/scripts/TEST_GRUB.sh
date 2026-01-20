#!/bin/bash
# Script para probar el kernel con GRUB localmente

cd "$(dirname "$0")"

if [ ! -f kernel.bin ]; then
    echo "❌ Error: kernel.bin no encontrado. Ejecuta ./build.sh primero."
    exit 1
fi

echo "=== Probando kernel con GRUB ==="
echo ""
echo "Verificando Multiboot header..."

# Verificar header
if objdump -s -j .multiboot_header kernel.bin | grep -q "1badb002"; then
    echo "✅ Multiboot header encontrado"
else
    echo "❌ Multiboot header NO encontrado"
    exit 1
fi

# Verificar posición en archivo
HEADER_OFFSET=$(readelf -l kernel.bin | grep -A 1 "LOAD" | head -2 | grep "0x0000000000001000" | wc -l)
if [ "$HEADER_OFFSET" -gt 0 ]; then
    echo "✅ Header está en los primeros segmentos"
else
    echo "⚠️  Header puede estar mal posicionado"
fi

echo ""
echo "Para probar en GRUB:"
echo "  1. Copia kernel.bin a /boot/"
echo "  2. O usa ./run_iso.sh para probar con la ISO"
