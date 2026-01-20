#!/bin/bash
# Script para abrir automáticamente el emulador QEMU con F3-OS

cd "$(dirname "$0")"

# Verificar que el kernel esté compilado
if [ ! -f kernel.bin ] && [ ! -f f3os.iso ]; then
    echo "❌ Error: kernel.bin o f3os.iso no encontrado"
    echo "Ejecuta primero: ./build.sh"
    exit 1
fi

# Verificar que el servidor GUI esté corriendo
if ! curl -s http://localhost:8080/api/status > /dev/null 2>&1; then
    echo "⚠️  Servidor GUI no está corriendo"
    echo "Iniciando servidor GUI en background..."
    cd agent
    ./run.sh gui-server > /tmp/f3os_gui.log 2>&1 &
    cd ..
    sleep 3
    echo "✅ Servidor GUI iniciado"
fi

echo "🚀 Abriendo emulador QEMU con F3-OS..."
echo "🌐 Servidor GUI accesible en: http://10.0.2.2:8080 (desde F3-OS)"
echo ""

# Abrir QEMU en una nueva ventana usando gnome-terminal o directamente
if command -v gnome-terminal &> /dev/null; then
    # Abrir en terminal separada
    gnome-terminal -- bash -c "
        cd $(pwd)
        if [ -f f3os.iso ]; then
            qemu-system-x86_64 -cdrom f3os.iso -display gtk -m 256M -no-reboot -machine type=pc,acpi=off,hpet=off -cpu qemu64 -boot order=d -no-shutdown -serial stdio -name 'F3-OS' -nodefaults -netdev user,id=net0,hostfwd=tcp::8080-:8080 -device rtl8139,netdev=net0
        else
            qemu-system-x86_64 -kernel kernel.bin -display gtk -m 256M -no-reboot -machine type=pc,acpi=off,hpet=off -cpu qemu64 -boot order=c -no-shutdown -serial stdio -name 'F3-OS' -nodefaults -netdev user,id=net0,hostfwd=tcp::8080-:8080 -device rtl8139,netdev=net0
        fi
        exec bash
    " &
else
    # Ejecutar directamente (abrirá ventana GTK)
    if [ -f f3os.iso ]; then
        qemu-system-x86_64 \
          -cdrom f3os.iso \
          -display gtk \
          -m 256M \
          -no-reboot \
          -machine type=pc,acpi=off,hpet=off \
          -cpu qemu64 \
          -boot order=d \
          -no-shutdown \
          -serial stdio \
          -name "F3-OS" \
          -nodefaults \
          -netdev user,id=net0,hostfwd=tcp::8080-:8080 \
          -device rtl8139,netdev=net0 &
    else
        qemu-system-x86_64 \
          -kernel kernel.bin \
          -display gtk \
          -m 256M \
          -no-reboot \
          -machine type=pc,acpi=off,hpet=off \
          -cpu qemu64 \
          -boot order=c \
          -no-shutdown \
          -serial stdio \
          -name "F3-OS" \
          -nodefaults \
          -netdev user,id=net0,hostfwd=tcp::8080-:8080 \
          -device rtl8139,netdev=net0 &
    fi
fi

echo "✅ Emulador iniciado"
echo "La ventana de QEMU debería abrirse automáticamente"

