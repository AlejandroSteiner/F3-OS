#!/bin/bash
# Script para iniciar automáticamente el sistema completo F3-OS
# Incluye: Servidor GUI del agente + Emulador QEMU

cd "$(dirname "$0")"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     F3-OS - Sistema Completo (Agente + Emulador)      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que el kernel esté compilado
if [ ! -f kernel.bin ] && [ ! -f f3os.iso ]; then
    echo -e "${RED}❌ Error: kernel.bin o f3os.iso no encontrado${NC}"
    echo "Ejecuta primero: ./build.sh"
    exit 1
fi

# Verificar si el servidor GUI está corriendo
GUI_PID=$(lsof -ti :8080 2>/dev/null)

if [ -z "$GUI_PID" ]; then
    echo -e "${YELLOW}📡 Servidor GUI no está corriendo. Iniciando...${NC}"
    
    # Iniciar servidor GUI en background
    cd agent
    ./run.sh gui-server > /tmp/f3os_gui_server.log 2>&1 &
    GUI_SERVER_PID=$!
    cd ..
    
    # Esperar a que el servidor esté listo
    echo -e "${YELLOW}⏳ Esperando a que el servidor GUI esté listo...${NC}"
    for i in {1..10}; do
        if curl -s http://localhost:8080/api/status > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Servidor GUI iniciado correctamente${NC}"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:8080/api/status > /dev/null 2>&1; then
        echo -e "${RED}❌ Error: No se pudo iniciar el servidor GUI${NC}"
        echo "Revisa los logs: /tmp/f3os_gui_server.log"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Servidor GUI ya está corriendo (PID: $GUI_PID)${NC}"
    GUI_SERVER_PID=$GUI_PID
fi

echo ""
echo -e "${GREEN}🌐 Servidor GUI accesible en:${NC}"
echo -e "   - Host: ${BLUE}http://localhost:8080${NC}"
echo -e "   - F3-OS (QEMU): ${BLUE}http://10.0.2.2:8080${NC}"
echo ""

# Función para limpiar al salir
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Cerrando sistema...${NC}"
    
    # Si iniciamos el servidor GUI, detenerlo
    if [ -n "$GUI_SERVER_PID" ] && [ "$GUI_SERVER_PID" != "$GUI_PID" ]; then
        echo -e "${YELLOW}Deteniendo servidor GUI...${NC}"
        kill $GUI_SERVER_PID 2>/dev/null
    fi
    
    echo -e "${GREEN}✅ Sistema cerrado${NC}"
}

trap cleanup EXIT INT TERM

# Iniciar QEMU
echo -e "${GREEN}🚀 Iniciando F3-OS en QEMU...${NC}"
echo ""
echo -e "${YELLOW}Controles:${NC}"
echo -e "   ${GREEN}Ctrl+Alt+G${NC} : Capturar/Liberar cursor"
echo -e "   ${GREEN}Ctrl+Alt+Q${NC} : Cerrar QEMU"
echo -e "   ${GREEN}Ctrl+Alt+2${NC} : Monitor de QEMU"
echo ""
echo -e "${YELLOW}⚠️  Al cerrar QEMU, el servidor GUI seguirá corriendo${NC}"
echo -e "${YELLOW}   Para detenerlo: cd agent && ./detener_servidor.sh${NC}"
echo ""

# Ejecutar QEMU
if [ -f f3os.iso ]; then
    echo -e "${YELLOW}Usando ISO booteable...${NC}"
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
      -device rtl8139,netdev=net0 \
      "$@"
else
    echo -e "${YELLOW}Intentando boot directo con Multiboot...${NC}"
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
      -device rtl8139,netdev=net0 \
      "$@"
fi

EXIT_CODE=$?

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ QEMU cerrado correctamente${NC}"
else
    echo -e "${YELLOW}⚠️  QEMU cerrado (código: $EXIT_CODE)${NC}"
fi

# El servidor GUI seguirá corriendo a menos que se haya iniciado aquí
if [ -n "$GUI_SERVER_PID" ] && [ "$GUI_SERVER_PID" != "$GUI_PID" ]; then
    echo -e "${YELLOW}El servidor GUI sigue corriendo en background${NC}"
    echo -e "${YELLOW}Para detenerlo: cd agent && ./detener_servidor.sh${NC}"
fi

echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"







