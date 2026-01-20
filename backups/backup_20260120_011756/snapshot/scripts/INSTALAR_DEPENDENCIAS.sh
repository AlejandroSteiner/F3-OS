#!/bin/bash
# Script para instalar todas las dependencias necesarias para F3-OS

echo "=== Instalando dependencias para F3-OS ==="
echo ""

# Instalar herramientas básicas
echo "📦 Instalando herramientas básicas..."
sudo apt update
sudo apt install -y \
    qemu-system-x86 \
    rustup \
    llvm \
    lld \
    xorriso \
    grub-pc-bin \
    grub-common \
    mtools

echo ""
echo "✅ Dependencias instaladas."
echo ""
echo "Ahora puedes:"
echo "  ./build.sh            # Compilar el kernel"
echo "  ./create_grub_iso.sh  # Crear ISO booteable"
echo "  ./run_iso.sh          # Ejecutar en QEMU"

