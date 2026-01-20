#!/bin/bash
# Script para crear ISO booteable con Limine

set -e

echo "=== Creando ISO booteable para F3-OS ==="
echo ""

# Verificar que kernel.bin existe
if [ ! -f kernel.bin ]; then
    echo "❌ Error: kernel.bin no encontrado. Ejecuta ./build.sh primero."
    exit 1
fi

# NOTA: Las versiones recientes de Limine no tienen binarios precompilados.
# Opción 1: Usar boot directo con QEMU (./run.sh) - NO REQUIERE LIMINE
# Opción 2: Compilar Limine localmente o descargar versión antigua (v5.x)

echo "⚠️  NOTA: Limine es externo y las versiones recientes no tienen binarios."
echo "   RECOMENDACIÓN: Usa ./run.sh para boot directo (no requiere Limine)"
echo ""

LIMINE_BIN_PATH=""

# Buscar binarios existentes
if [ -f limine/bin/limine-bios.sys ]; then
    LIMINE_BIN_PATH="limine/bin"
    echo "✅ Limine encontrado localmente"
elif [ -f limine/limine-bios.sys ]; then
    LIMINE_BIN_PATH="limine"
    echo "✅ Limine encontrado localmente"
elif [ -d limine ] && [ -f limine/GNUmakefile ]; then
    echo "📦 Limine código fuente encontrado. Compilando..."
    cd limine
    if [ -f bootstrap ]; then
        ./bootstrap 2>/dev/null || true
    fi
    if [ -f GNUmakefile ]; then
        make -f GNUmakefile 2>/dev/null || make 2>/dev/null || {
            cd ..
            echo "⚠️  No se pudo compilar Limine. Usa ./run.sh para boot directo."
            exit 1
        }
    fi
    cd ..
    if [ -f limine/bin/limine-bios.sys ]; then
        LIMINE_BIN_PATH="limine/bin"
        echo "✅ Limine compilado exitosamente"
    elif [ -f limine/limine-bios.sys ]; then
        LIMINE_BIN_PATH="limine"
        echo "✅ Limine compilado exitosamente"
    fi
fi

if [ -z "$LIMINE_BIN_PATH" ]; then
    echo "⚠️  Limine no disponible. Opciones:"
    echo "   1. Ejecuta ./run.sh para boot directo (RECOMENDADO)"
    echo "   2. Compila Limine manualmente:"
    echo "      git clone https://github.com/limine-bootloader/limine.git"
    echo "      cd limine && ./bootstrap && ./configure && make"
    echo "   3. Descarga versión antigua con binarios: v5.20240909.0"
    echo ""
    read -p "¿Deseas continuar creando ISO sin Limine? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[SsYy]$ ]]; then
        exit 0
    fi
    echo "⚠️  Continuando sin Limine. La ISO puede no bootear correctamente."
else
    echo "📦 Descargando binarios precompilados de Limine (EXTERNO, no es parte de F3-OS)..."
    
    # Obtener la última versión de Limine
    if command -v curl &> /dev/null; then
        LIMINE_VERSION=$(curl -s https://api.github.com/repos/limine-bootloader/limine/releases/latest | grep '"tag_name"' | cut -d'"' -f4 | head -1)
    elif command -v wget &> /dev/null; then
        LIMINE_VERSION=$(wget -qO- https://api.github.com/repos/limine-bootloader/limine/releases/latest | grep '"tag_name"' | cut -d'"' -f4 | head -1)
    fi
    
    # Si no se pudo obtener, usar versión conocida
    if [ -z "$LIMINE_VERSION" ]; then
        LIMINE_VERSION="v7.7.3"
    fi
    
    echo "   Versión: $LIMINE_VERSION"
    
    # Obtener URL real del asset desde la API de GitHub
    echo "   Obteniendo URL del asset..."
    LIMINE_URL=""
    
    if command -v python3 &> /dev/null; then
        # Buscar asset que contenga x86_64 o bin en el nombre y sea tar.gz
        LIMINE_URL=$(curl -s "https://api.github.com/repos/limine-bootloader/limine/releases/latest" | \
            python3 -c "import sys, json; data = json.load(sys.stdin); assets = data.get('assets', []); \
            url = [a['browser_download_url'] for a in assets if ('x86_64' in a['name'].lower() or 'bin' in a['name'].lower()) and 'tar.gz' in a['name'].lower() and 'sig' not in a['name'].lower()]; \
            print(url[0] if url else '')" 2>/dev/null)
        
        # Si no hay binarios específicos, buscar cualquier tar.gz (fuentes)
        if [ -z "$LIMINE_URL" ]; then
            LIMINE_URL=$(curl -s "https://api.github.com/repos/limine-bootloader/limine/releases/latest" | \
                python3 -c "import sys, json; data = json.load(sys.stdin); assets = data.get('assets', []); \
                url = [a['browser_download_url'] for a in assets if 'tar.gz' in a['name'].lower() and 'sig' not in a['name'].lower()]; \
                print(url[0] if url else '')" 2>/dev/null)
        fi
    fi
    
    # Si Python falló o no hay URL, usar versión conocida que tiene binarios
    if [ -z "$LIMINE_URL" ]; then
        # Usar versión v7.7.3 que sabemos que tiene binarios precompilados
        LIMINE_VERSION="v7.7.3"
        LIMINE_URL="https://github.com/limine-bootloader/limine/releases/download/${LIMINE_VERSION}/limine-${LIMINE_VERSION}-x86_64-bin.tar.gz"
        echo "   Usando versión conocida: $LIMINE_VERSION"
    fi
    
    if [ -z "$LIMINE_URL" ]; then
        echo "❌ Error: No se pudo encontrar URL válida para descargar Limine."
        echo "   Descarga manualmente desde:"
        echo "   https://github.com/limine-bootloader/limine/releases"
        echo "   Extrae los binarios a limine/bin/"
        exit 1
    fi
    
    echo "   URL: $LIMINE_URL"
    
    # Descargar
    DOWNLOADED=0
    if command -v wget &> /dev/null; then
        if wget -q "${LIMINE_URL}" -O /tmp/limine.tar.gz 2>/dev/null && [ -s /tmp/limine.tar.gz ]; then
            DOWNLOADED=1
        fi
    fi
    
    if [ $DOWNLOADED -eq 0 ] && command -v curl &> /dev/null; then
        if curl -L -s "${LIMINE_URL}" -o /tmp/limine.tar.gz 2>/dev/null && [ -s /tmp/limine.tar.gz ]; then
            DOWNLOADED=1
        fi
    fi
    
    if [ $DOWNLOADED -eq 0 ] || [ ! -s /tmp/limine.tar.gz ]; then
        echo "❌ Error: No se pudo descargar Limine o el archivo está vacío."
        echo "   Verifica tu conexión a internet o descarga manualmente desde:"
        echo "   https://github.com/limine-bootloader/limine/releases"
        exit 1
    fi
    
    # Verificar que el archivo descargado es válido
    if [ ! -f /tmp/limine.tar.gz ] || [ ! -s /tmp/limine.tar.gz ]; then
        echo "❌ Error: Archivo descargado está vacío o no existe."
        exit 1
    fi
    
    # Verificar tipo de archivo
    FILE_TYPE=$(file /tmp/limine.tar.gz | grep -o "gzip\|gzip compressed")
    if [ -z "$FILE_TYPE" ]; then
        echo "⚠️  El archivo puede no ser un tar.gz válido. Verificando..."
        if grep -q "Not Found\|404" /tmp/limine.tar.gz 2>/dev/null; then
            echo "❌ Error: URL no encontrada. La versión puede no tener binarios precompilados."
            echo "   Intenta usar una versión específica o descarga manualmente."
            exit 1
        fi
    fi
    
    # Extraer binarios
    echo "📂 Extrayendo binarios..."
    mkdir -p limine
    cd limine
    
    # Intentar extraer con verbose para ver errores
    if ! tar -xzf /tmp/limine.tar.gz 2>&1; then
        echo "⚠️  Error extrayendo con tar. Intentando método alternativo..."
        # Intentar sin compresión gzip (por si acaso)
        tar -xf /tmp/limine.tar.gz 2>&1 || {
            cd ..
            echo "❌ Error: No se pudo extraer el archivo."
            echo "   Tamaño del archivo: $(ls -lh /tmp/limine.tar.gz | awk '{print $5}')"
            echo "   Tipo: $(file /tmp/limine.tar.gz)"
            echo "   Intenta descargar manualmente desde:"
            echo "   https://github.com/limine-bootloader/limine/releases"
            exit 1
        }
    fi
    cd ..
    
    # Buscar binarios extraídos (múltiples posibles ubicaciones)
    if [ -f limine/bin/limine-bios.sys ]; then
        LIMINE_BIN_PATH="limine/bin"
    elif [ -f limine/limine-bios.sys ]; then
        LIMINE_BIN_PATH="limine"
    else
        # Buscar en subdirectorios
        LIMINE_BIN_FILE=$(find limine -name "limine-bios.sys" -type f | head -1)
        if [ -n "$LIMINE_BIN_FILE" ]; then
            LIMINE_BIN_PATH=$(dirname "$LIMINE_BIN_FILE")
            # Mover a ubicación estándar si está en subdirectorio
            if [ "$LIMINE_BIN_PATH" != "limine" ] && [ "$LIMINE_BIN_PATH" != "limine/bin" ]; then
                cp -r "${LIMINE_BIN_PATH}"/* limine/bin/ 2>/dev/null || mkdir -p limine/bin && cp -r "${LIMINE_BIN_PATH}"/* limine/bin/
                LIMINE_BIN_PATH="limine/bin"
            fi
        fi
    fi
    
    if [ -z "$LIMINE_BIN_PATH" ] || [ ! -f "${LIMINE_BIN_PATH}/limine-bios.sys" ]; then
        echo "❌ Error: No se encontraron binarios de Limine después de extraer."
        echo "   Intenta descargar manualmente desde:"
        echo "   https://github.com/limine-bootloader/limine/releases"
        exit 1
    fi
    
    echo "✅ Limine descargado en: $LIMINE_BIN_PATH"
fi

# Crear estructura de ISO
echo "📁 Creando estructura de ISO..."
rm -rf iso
mkdir -p iso/boot

# Copiar kernel y configuración
cp kernel.bin iso/boot/kernel
cp boot/limine.cfg iso/boot/

# Copiar binarios de Limine
cp "${LIMINE_BIN_PATH}/limine-bios.sys" iso/
if [ -f "${LIMINE_BIN_PATH}/limine-bios-cd.bin" ]; then
    cp "${LIMINE_BIN_PATH}/limine-bios-cd.bin" iso/
elif [ -f "${LIMINE_BIN_PATH}/limine-cd-eltorito.bin" ]; then
    cp "${LIMINE_BIN_PATH}/limine-cd-eltorito.bin" iso/limine-bios-cd.bin
fi

# Buscar herramienta limine
LIMINE_TOOL=""
if [ -f limine/limine ]; then
    LIMINE_TOOL="limine/limine"
elif [ -f "${LIMINE_BIN_PATH}/limine" ]; then
    LIMINE_TOOL="${LIMINE_BIN_PATH}/limine"
elif [ -f /tmp/limine-*/bin/limine ]; then
    LIMINE_TOOL=$(find /tmp/limine-*/bin/limine | head -1)
fi

# Crear ISO
echo "💿 Creando ISO..."
if ! command -v xorriso &> /dev/null; then
    echo "❌ Error: xorriso no encontrado. Instala con:"
    echo "  sudo apt install -y xorriso"
    exit 1
fi

# Determinar el nombre del archivo boot
BOOT_FILE="limine-bios-cd.bin"
if [ ! -f "iso/${BOOT_FILE}" ]; then
    BOOT_FILE="limine-cd-eltorito.bin"
fi

xorriso -as mkisofs \
  -b "${BOOT_FILE}" \
  -no-emul-boot \
  -boot-load-size 4 \
  -boot-info-table \
  --protective-msdos-label \
  iso -o f3os.iso

# Instalar Limine en la ISO
echo "🔧 Instalando Limine en ISO..."
if [ -n "$LIMINE_TOOL" ] && [ -f "$LIMINE_TOOL" ]; then
    "$LIMINE_TOOL" bios-install f3os.iso
else
    echo "⚠️  Herramienta limine no encontrada. La ISO puede no bootear correctamente."
fi

echo ""
echo "✅ ISO creada: f3os.iso"
echo ""
echo "Para ejecutar en QEMU:"
echo "  qemu-system-x86_64 -cdrom f3os.iso -display gtk -m 256M"
echo ""
echo "O usar:"
echo "  ./run_iso.sh"

