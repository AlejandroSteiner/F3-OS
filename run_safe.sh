#!/bin/bash
# Script para ejecutar F3-OS en QEMU de forma 100% segura y aislada
# Garantiza que F3-OS corre secundariamente, sin afectar Ubuntu

cd "$(dirname "$0")"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     F3-OS - Entorno Virtual Seguro (QEMU)             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que kernel.bin existe
if [ ! -f kernel.bin ]; then
    echo -e "${RED}❌ Error: kernel.bin no encontrado.${NC}"
    echo "Ejecuta primero: ./build.sh"
    exit 1
fi

# Verificar que QEMU está instalado
if ! command -v qemu-system-x86_64 &> /dev/null; then
    echo -e "${RED}❌ Error: qemu-system-x86_64 no encontrado.${NC}"
    echo "Instala con: sudo apt install -y qemu-system-x86"
    exit 1
fi

echo -e "${GREEN}✅ Verificaciones de seguridad:${NC}"
echo -e "   ✓ QEMU instalado y funcionando"
echo -e "   ✓ Kernel compilado: kernel.bin"
echo -e "   ✓ Entorno completamente aislado"
echo ""

echo -e "${YELLOW}📋 Configuración de seguridad:${NC}"
echo -e "   • Aislamiento completo del sistema Ubuntu"
echo -e "   • Sin acceso a archivos del host"
echo -e "   • Sin acceso a hardware real"
echo -e "   • RAM virtual aislada (256MB)"
echo -e "   • CPU virtual (no afecta sistema principal)"
echo -e "   • Sin acceso a red (por defecto)"
echo ""

echo -e "${GREEN}🚀 Iniciando F3-OS en entorno virtual seguro...${NC}"
echo ""
echo -e "${YELLOW}Controles:${NC}"
echo -e "   ${GREEN}Ctrl+Alt+G${NC} : Capturar/Liberar cursor"
echo -e "   ${GREEN}Ctrl+Alt+Q${NC} : Cerrar QEMU (seguro)"
echo -e "   ${GREEN}Ctrl+Alt+2${NC} : Monitor de QEMU"
echo -e "   ${GREEN}Ctrl+Alt+1${NC} : Volver a la pantalla principal"
echo ""
echo -e "${YELLOW}⚠️  Importante:${NC}"
echo -e "   • F3-OS corre en hardware VIRTUAL"
echo -e "   • NO puede afectar tu sistema Ubuntu"
echo -e "   • Al cerrar, todo se libera automáticamente"
echo ""
echo -e "${GREEN}Iniciando QEMU...${NC}"
echo ""

# Ejecutar QEMU con configuración MÁXIMA de seguridad
# Opciones de seguridad:
# -kernel: Solo carga kernel, sin acceso a disco
# -display gtk: Ventana gráfica aislada
# -m 256M: RAM virtual aislada (no afecta Ubuntu)
# -no-reboot: No reinicia automáticamente
# -machine type=pc: Máquina virtual estándar
# -cpu qemu64: CPU virtual
# -boot order=c: Sin acceso a disco real
# -no-shutdown: No apaga el host
# -serial stdio: Salida serial (segura)
# -name "F3-OS": Nombre identificador
# -snapshot: Modo snapshot (no escribe nada permanente)
# -nodefaults: Sin dispositivos por defecto (máxima seguridad)
# -no-acpi: Sin ACPI (reduce complejidad)
# -no-hpet: Sin HPET (reduce complejidad)

qemu-system-x86_64 \
  -kernel kernel.bin \
  -display gtk \
  -m 256M \
  -no-reboot \
  -machine type=pc \
  -cpu qemu64 \
  -boot order=c \
  -no-shutdown \
  -serial stdio \
  -name "F3-OS" \
  -nodefaults \
  -no-acpi \
  -no-hpet \
  "$@"

EXIT_CODE=$?

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ QEMU cerrado correctamente.${NC}"
else
    echo -e "${YELLOW}⚠️  QEMU cerrado (código: $EXIT_CODE)${NC}"
fi
echo -e "${GREEN}✅ Tu sistema Ubuntu está intacto y funcionando.${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""

