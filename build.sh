#!/bin/bash
set -e

echo "Building F3-OS kernel..."

# Check for Rust
if ! command -v rustc &> /dev/null; then
    echo "Error: Rust not found. Install with:"
    echo "  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
    exit 1
fi

# Set up Rust nightly
echo "Setting up Rust nightly..."
rustup toolchain install nightly --profile minimal 2>/dev/null || true
rustup default nightly 2>/dev/null || true
rustup component add rust-src --toolchain nightly-x86_64-unknown-linux-gnu 2>/dev/null || true

# Check for target
if [ ! -f x86_64-unknown-none.json ]; then
    echo "Error: x86_64-unknown-none.json not found"
    exit 1
fi

# Build kernel
echo "Compiling kernel..."
cd kernel

# Verificar que existe el linker script
if [ ! -f linker.ld ]; then
    echo "Error: linker.ld not found in kernel/"
    exit 1
fi

# Obtener ruta absoluta del linker script (necesario para que el linker lo encuentre)
LINKER_SCRIPT=$(pwd)/linker.ld
echo "Linker script: $LINKER_SCRIPT"

# Verificar que rust-lld está disponible
if ! command -v rust-lld &> /dev/null && ! command -v ld.lld &> /dev/null; then
    echo "Error: rust-lld not found. Installing lld..."
    sudo apt install -y lld || {
        echo "Failed to install lld. Please install manually:"
        echo "  sudo apt install -y lld"
        exit 1
    }
fi

# Construir con build-std para target custom (requerido para targets personalizados)
echo "Building with build-std (required for custom target)..."
echo "Target: bare metal kernel for QEMU emulator"

# Usar ruta absoluta del linker script
export RUSTFLAGS="-C link-arg=-T${LINKER_SCRIPT}"
cargo +nightly build \
  --target ../x86_64-unknown-none.json \
  -Z build-std=core,alloc,compiler_builtins

BUILD_STATUS=$?
if [ $BUILD_STATUS -ne 0 ]; then
    echo "Build failed. Check errors above."
    exit 1
fi

cd ..

# Copy kernel binary (buscar en diferentes ubicaciones posibles)
KERNEL_BIN=""
if [ -f target/x86_64-unknown-none/debug/f3-kernel ]; then
    KERNEL_BIN="target/x86_64-unknown-none/debug/f3-kernel"
elif [ -f kernel/target/x86_64-unknown-none/debug/f3-kernel ]; then
    KERNEL_BIN="kernel/target/x86_64-unknown-none/debug/f3-kernel"
elif [ -f target/x86_64-unknown-none/release/f3-kernel ]; then
    KERNEL_BIN="target/x86_64-unknown-none/release/f3-kernel"
elif [ -f kernel/target/x86_64-unknown-none/release/f3-kernel ]; then
    KERNEL_BIN="kernel/target/x86_64-unknown-none/release/f3-kernel"
fi

if [ -n "$KERNEL_BIN" ] && [ -f "$KERNEL_BIN" ]; then
    cp "$KERNEL_BIN" kernel.bin
    echo ""
    echo "✅ Kernel built successfully: kernel.bin"
    echo "   Source: $KERNEL_BIN"
else
    echo ""
    echo "❌ Error: kernel binary not found."
    echo "   Searched in:"
    echo "     - target/x86_64-unknown-none/debug/f3-kernel"
    echo "     - kernel/target/x86_64-unknown-none/debug/f3-kernel"
    echo "     - target/x86_64-unknown-none/release/f3-kernel"
    echo "     - kernel/target/x86_64-unknown-none/release/f3-kernel"
    exit 1
fi

echo ""
echo "To run in QEMU:"
echo "  qemu-system-x86_64 -kernel kernel.bin -display gtk -m 256M -no-reboot"
echo ""
echo "Or use the run script:"
echo "  ./run.sh"

