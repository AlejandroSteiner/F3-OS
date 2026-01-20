#!/bin/bash
# Script de instalación automática para Ubuntu 24.04 LTS

set -e

echo "=== Instalación de F3-OS en Ubuntu 24.04 LTS ==="
echo ""

# Verificar que estamos en Ubuntu
if [ ! -f /etc/os-release ]; then
    echo "Error: No se puede detectar el sistema operativo"
    exit 1
fi

source /etc/os-release
if [ "$ID" != "ubuntu" ]; then
    echo "Advertencia: Este script está optimizado para Ubuntu"
fi

echo "Instalando dependencias..."
echo ""

# Actualizar repositorios
sudo apt update

# Instalar QEMU
echo "📦 Instalando QEMU..."
sudo apt install -y qemu-system-x86 qemu-kvm

# Instalar herramientas de build
echo "📦 Instalando herramientas de compilación..."
sudo apt install -y build-essential llvm lld

# Instalar herramientas opcionales
echo "📦 Instalando herramientas opcionales..."
sudo apt install -y xorriso grub-pc-bin nasm

# Instalar Rust
if ! command -v rustc &> /dev/null; then
    echo "📦 Instalando Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source $HOME/.cargo/env
else
    echo "✅ Rust ya está instalado"
    source $HOME/.cargo/env 2>/dev/null || true
fi

# Configurar Rust Nightly
echo "📦 Configurando Rust Nightly..."
rustup toolchain install nightly --profile minimal
rustup default nightly
rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Verificar instalación:"
echo "  qemu-system-x86_64 --version"
echo "  rustc --version"
echo ""
echo "Ahora puedes compilar F3-OS:"
echo "  cd /home/ktzchen/Documentos/f3-os"
echo "  ./build.sh"
echo "  ./run.sh"

