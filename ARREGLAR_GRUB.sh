#!/bin/bash
# Script para diagnosticar y arreglar el problema de GRUB con Multiboot header

cd "$(dirname "$0")"

echo "=== Diagnóstico de Problema con GRUB ==="
echo ""

if [ ! -f kernel.bin ]; then
    echo "❌ Error: kernel.bin no encontrado."
    exit 1
fi

if [ ! -f f3os.iso ]; then
    echo "❌ Error: f3os.iso no encontrada."
    echo "Ejecuta primero: ./create_grub_iso.sh"
    exit 1
fi

echo "1. Verificando Multiboot header en kernel.bin..."
if objdump -s -j .multiboot_header kernel.bin 2>/dev/null | grep -q "1badb002\|02b0ad1b"; then
    echo "   ✅ Multiboot header encontrado en kernel.bin"
else
    echo "   ❌ Multiboot header NO encontrado en kernel.bin"
    exit 1
fi

echo ""
echo "2. Verificando posición del header en archivo..."
HEADER_OFFSET=$(objdump -h kernel.bin | grep multiboot_header | awk '{print $6}')
echo "   Offset del header: $HEADER_OFFSET"

# Verificar si está en los primeros 8KB (8192 bytes = 0x2000)
if [ -n "$HEADER_OFFSET" ]; then
    OFFSET_DEC=$(echo "ibase=16; $(echo $HEADER_OFFSET | tr '[:lower:]' '[:upper:]')" | bc 2>/dev/null || echo "$HEADER_OFFSET")
    if [ "$OFFSET_DEC" -lt 8192 ] 2>/dev/null; then
        echo "   ✅ Header está en los primeros 8KB del archivo"
    else
        echo "   ⚠️  Header puede estar fuera de los primeros 8KB"
    fi
fi

echo ""
echo "3. Verificando archivos en estructura ISO..."
if [ -d iso/boot ]; then
    echo "   ✅ Estructura ISO existe"
    if [ -f iso/boot/kernel.bin ]; then
        echo "   ✅ kernel.bin está en iso/boot/"
        if objdump -s -j .multiboot_header iso/boot/kernel.bin 2>/dev/null | grep -q "1badb002\|02b0ad1b"; then
            echo "   ✅ Multiboot header presente en kernel.bin de ISO"
        else
            echo "   ❌ Multiboot header NO encontrado en kernel.bin de ISO"
            echo "   Esto puede indicar que el archivo se corrompió al copiarlo"
        fi
    else
        echo "   ❌ kernel.bin NO encontrado en iso/boot/"
    fi
else
    echo "   ❌ Estructura ISO no existe"
fi

echo ""
echo "4. Verificando configuración de GRUB..."
if [ -f iso/boot/grub/grub.cfg ]; then
    echo "   ✅ grub.cfg existe"
    if grep -q "multiboot" iso/boot/grub/grub.cfg; then
        echo "   ✅ grub.cfg contiene comando multiboot"
    else
        echo "   ❌ grub.cfg NO contiene comando multiboot"
    fi
else
    echo "   ❌ grub.cfg no encontrado"
fi

echo ""
echo "=== Recomendaciones ==="
echo ""
echo "Si todos los checks pasan pero GRUB aún falla:"
echo "  1. Prueba la opción 'F3-OS (verificar)' en el menú de GRUB"
echo "  2. Presiona 'c' en GRUB para entrar a la línea de comandos"
echo "  3. Prueba manualmente:"
echo "     multiboot (cd0)/boot/kernel.bin"
echo "     boot"
echo ""
echo "Si el header no está en los primeros 8KB:"
echo "  - Puede ser necesario ajustar el linker script"
echo "  - O usar un bootloader diferente (Limine)"
