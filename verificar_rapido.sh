#!/bin/bash
# Verificación Rápida del Sistema F3-OS (30 segundos)

echo "🔍 Verificación Rápida F3-OS"
echo "=============================="
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Agente
echo "🤖 Verificando agente..."
cd agent 2>/dev/null && ./run.sh status > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Agente funcionando${NC}"
else
    echo -e "${RED}❌ Agente no responde${NC}"
fi
cd .. 2>/dev/null

# 2. Kernel
echo "🔧 Verificando kernel..."
if [ -f "kernel.bin" ] && [ -f "f3os.iso" ]; then
    echo -e "${GREEN}✅ Kernel e ISO compilados${NC}"
else
    echo -e "${YELLOW}⚠️  Kernel no compilado (ejecuta ./build.sh)${NC}"
fi

# 3. Herramientas
echo "🛠️  Verificando herramientas..."
TOOLS_OK=0
command -v python3 &> /dev/null && TOOLS_OK=$((TOOLS_OK + 1))
command -v rustc &> /dev/null && TOOLS_OK=$((TOOLS_OK + 1))
command -v qemu-system-x86_64 &> /dev/null && TOOLS_OK=$((TOOLS_OK + 1))

if [ $TOOLS_OK -eq 3 ]; then
    echo -e "${GREEN}✅ Todas las herramientas instaladas${NC}"
elif [ $TOOLS_OK -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Faltan algunas herramientas${NC}"
else
    echo -e "${RED}❌ Faltan herramientas críticas${NC}"
fi

echo ""
echo "=============================="
echo "✅ Verificación rápida completada"
echo ""
echo "Para verificación completa: ./verificar_sistema.sh"






