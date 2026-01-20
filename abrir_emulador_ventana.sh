#!/bin/bash
# Script para abrir QEMU en una ventana visible

cd "$(dirname "$0")"

# Verificar servidor GUI
if ! curl -s http://localhost:8080/api/status > /dev/null 2>&1; then
    echo "Iniciando servidor GUI..."
    cd agent && ./run.sh gui-server > /dev/null 2>&1 & cd ..
    sleep 3
fi

# Ejecutar QEMU directamente (abrirá ventana GTK)
if [ -f f3os.iso ]; then
    exec qemu-system-x86_64 \
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
      -netdev user,id=net0 \
      -device rtl8139,netdev=net0
else
    exec qemu-system-x86_64 \
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
      -netdev user,id=net0 \
      -device rtl8139,netdev=net0
fi
