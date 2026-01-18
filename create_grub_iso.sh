#!/bin/bash
# Script para crear ISO booteable con GRUB (más simple que Limine)

set -e

echo "=== Creando ISO booteable para F3-OS con GRUB ==="
echo ""

# Verificar que kernel.bin existe
if [ ! -f kernel.bin ]; then
    echo "❌ Error: kernel.bin no encontrado. Ejecuta ./build.sh primero."
    exit 1
fi

# Verificar que GRUB está instalado
if ! command -v grub-mkrescue &> /dev/null && ! command -v grub2-mkrescue &> /dev/null; then
    echo "❌ Error: grub-mkrescue no encontrado."
    echo "Instala con: sudo apt install -y grub-pc-bin grub-common xorriso mtools"
    exit 1
fi

# Verificar que mtools está instalado (necesario para grub-mkrescue)
if ! command -v mformat &> /dev/null; then
    echo "⚠️  mtools no encontrado (necesario para grub-mkrescue)."
    echo "Instala con: sudo apt install -y mtools"
    exit 1
fi

echo "📁 Creando estructura de ISO..."
rm -rf iso
mkdir -p iso/boot/grub

# Copiar kernel
cp kernel.bin iso/boot/kernel.bin

# Crear configuración GRUB
cat > iso/boot/grub/grub.cfg << 'EOF'
set timeout=3
set default=0
set gfxpayload=text

# Configurar root
set root=(cd0)

menuentry "F3-OS" {
    # Cargar módulos necesarios
    insmod multiboot
    insmod normal
    insmod part_msdos
    insmod ext2
    insmod iso9660
    
    echo "Cargando kernel F3-OS..."
    # Usar ruta absoluta explícita
    multiboot ($root)/boot/kernel.bin
    echo "Kernel cargado. Iniciando F3-OS..."
    boot
}

menuentry "F3-OS (verificar archivos)" {
    insmod ls
    insmod multiboot
    echo "=== Verificando archivos en ISO ==="
    ls /
    ls /boot/
    echo ""
    echo "Presiona cualquier tecla para arrancar..."
    read
    multiboot ($root)/boot/kernel.bin
    boot
}

menuentry "F3-OS (línea de comandos GRUB)" {
    echo "Entrando a línea de comandos de GRUB..."
    echo "Usa estos comandos:"
    echo "  multiboot (cd0)/boot/kernel.bin"
    echo "  boot"
}
EOF

echo "💿 Creando ISO con GRUB..."
GRUB_MKRESCUE=""
if command -v grub-mkrescue &> /dev/null; then
    GRUB_MKRESCUE="grub-mkrescue"
elif command -v grub2-mkrescue &> /dev/null; then
    GRUB_MKRESCUE="grub2-mkrescue"
else
    echo "❌ Error: grub-mkrescue no encontrado."
    exit 1
fi

# Crear ISO (capturar stderr para ver errores reales)
echo "   Ejecutando $GRUB_MKRESCUE..."
if $GRUB_MKRESCUE -o f3os.iso iso > /tmp/grub_mkrescue.log 2>&1; then
    echo "   ISO creada exitosamente"
else
    echo "❌ Error al crear ISO. Detalles:"
    cat /tmp/grub_mkrescue.log | grep -v "^xorriso\|^grub-mkrescue\|^MKRESCUE\|^Input\|^Output" | head -20
    echo ""
    echo "Verifica:"
    echo "  - Que xorriso está instalado: sudo apt install -y xorriso"
    echo "  - Que los archivos están en iso/boot/grub/"
    exit 1
fi

if [ ! -f f3os.iso ]; then
    echo "❌ Error: No se pudo crear la ISO (archivo no existe)."
    echo "Log completo en /tmp/grub_mkrescue.log"
    exit 1
fi

# Verificar tamaño de la ISO
ISO_SIZE=$(stat -f%z f3os.iso 2>/dev/null || stat -c%s f3os.iso 2>/dev/null || echo "0")
if [ "$ISO_SIZE" -lt 1024 ]; then
    echo "❌ Error: La ISO es demasiado pequeña (${ISO_SIZE} bytes)."
    echo "Log completo en /tmp/grub_mkrescue.log"
    exit 1
fi

echo "   Tamaño de ISO: $(du -h f3os.iso | cut -f1)"

echo ""
echo "✅ ISO creada: f3os.iso"
echo ""
echo "Para ejecutar en QEMU:"
echo "  qemu-system-x86_64 -cdrom f3os.iso -display gtk -m 256M"
echo ""
echo "O usar:"
echo "  ./run_iso.sh"

