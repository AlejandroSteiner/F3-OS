#!/bin/bash
# Script de Verificación del Sistema F3-OS
# Verifica que todos los componentes estén funcionando correctamente

echo "🔍 Verificando Sistema F3-OS..."
echo "=================================="
echo ""

ERRORS=0
WARNINGS=0

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1${NC}"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

# 1. Verificar estructura del proyecto
echo "📁 Verificando estructura del proyecto..."
[ -d "kernel" ] && check "Directorio kernel existe" || warn "Directorio kernel no encontrado"
[ -d "agent" ] && check "Directorio agent existe" || warn "Directorio agent no encontrado"
[ -f "build.sh" ] && check "Script build.sh existe" || warn "Script build.sh no encontrado"
echo ""

# 2. Verificar kernel
echo "🔧 Verificando kernel..."
if [ -f "kernel.bin" ]; then
    check "kernel.bin compilado"
    file kernel.bin | grep -q "ELF" && check "kernel.bin es un binario ELF válido" || warn "kernel.bin no es un binario ELF válido"
else
    warn "kernel.bin no encontrado (ejecuta ./build.sh para compilar)"
fi

if [ -f "f3os.iso" ]; then
    check "ISO booteable (f3os.iso) existe"
else
    warn "ISO no encontrada (ejecuta ./create_grub_iso.sh para crear)"
fi
echo ""

# 3. Verificar agente
echo "🤖 Verificando agente gobernante..."
cd agent 2>/dev/null || { echo "❌ No se puede acceder al directorio agent"; exit 1; }

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    check "Python 3 instalado (versión $PYTHON_VERSION)"
else
    warn "Python 3 no encontrado"
fi

# Verificar entorno virtual
if [ -d "venv" ]; then
    check "Entorno virtual existe"
    if [ -f "venv/bin/activate" ]; then
        check "Entorno virtual es válido"
    fi
else
    warn "Entorno virtual no encontrado (se creará automáticamente al ejecutar ./run.sh)"
fi

# Verificar configuración
if [ -f "config/config.yaml" ]; then
    check "Archivo de configuración existe"
    
    # Verificar token de GitHub (opcional)
    if grep -q "token:" config/config.yaml 2>/dev/null; then
        TOKEN=$(grep "token:" config/config.yaml | head -1 | awk '{print $2}' | tr -d '"')
        if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ] && [ "$TOKEN" != "TU_TOKEN_AQUI" ]; then
            check "Token de GitHub configurado"
        else
            warn "Token de GitHub no configurado (opcional, para funcionalidad completa)"
        fi
    else
        warn "Token de GitHub no configurado (opcional)"
    fi
else
    warn "Archivo de configuración no encontrado (se creará automáticamente)"
fi

# Verificar dependencias
if [ -d "venv" ]; then
    source venv/bin/activate 2>/dev/null
    python3 -c "import yaml" 2>/dev/null && check "PyYAML instalado" || warn "PyYAML no instalado"
    python3 -c "import psutil" 2>/dev/null && check "psutil instalado" || warn "psutil no instalado"
    python3 -c "from github import Github" 2>/dev/null && check "PyGithub instalado" || warn "PyGithub no instalado"
    deactivate 2>/dev/null
else
    warn "No se puede verificar dependencias (entorno virtual no existe)"
fi

# Verificar módulos del agente
echo ""
echo "📦 Verificando módulos del agente..."
[ -f "src/main.py" ] && check "main.py existe" || warn "main.py no encontrado"
[ -f "src/governance_core.py" ] && check "governance_core.py existe" || warn "governance_core.py no encontrado"
[ -f "src/gui_assistant.py" ] && check "gui_assistant.py existe" || warn "gui_assistant.py no encontrado"
[ -f "src/project_analyzer.py" ] && check "project_analyzer.py existe" || warn "project_analyzer.py no encontrado"
[ -f "src/gui_server.py" ] && check "gui_server.py existe" || warn "gui_server.py no encontrado"
echo ""

# 4. Probar ejecución del agente (sin iniciar servidor)
echo "🧪 Probando ejecución del agente..."
cd "$(dirname "$0")/agent" 2>/dev/null || cd agent
if [ -f "run.sh" ]; then
    # Probar comando status (no inicia servidor)
    timeout 5 ./run.sh status > /dev/null 2>&1
    if [ $? -eq 0 ] || [ $? -eq 124 ]; then
        check "Agente puede ejecutarse (status)"
    else
        warn "Agente tiene problemas al ejecutarse"
    fi
else
    warn "Script run.sh no encontrado"
fi
echo ""

# 5. Verificar archivos de documentación clave
cd "$(dirname "$0")" 2>/dev/null || cd ..
echo "📚 Verificando documentación..."
[ -f "MANIFIESTO.md" ] && check "MANIFIESTO.md existe" || warn "MANIFIESTO.md no encontrado"
[ -f "REGLAS_LOGICA.md" ] && check "REGLAS_LOGICA.md existe" || warn "REGLAS_LOGICA.md no encontrado"
[ -f "README.md" ] && check "README.md existe" || warn "README.md no encontrado"
echo ""

# 6. Verificar herramientas de build
echo "🛠️  Verificando herramientas de build..."
command -v rustc &> /dev/null && check "Rust instalado" || warn "Rust no encontrado (necesario para compilar kernel)"
command -v cargo &> /dev/null && check "Cargo instalado" || warn "Cargo no encontrado (necesario para compilar kernel)"
command -v qemu-system-x86_64 &> /dev/null && check "QEMU instalado" || warn "QEMU no encontrado (necesario para ejecutar F3-OS)"
echo ""

# Resumen
echo "=================================="
echo "📊 Resumen de Verificación"
echo "=================================="

if [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  Advertencias: $WARNINGS${NC}"
fi

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ Errores: $ERRORS${NC}"
    echo ""
    echo "💡 Algunos componentes necesitan atención."
    exit 1
else
    echo ""
    echo -e "${GREEN}✅ Sistema verificado correctamente${NC}"
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Hay $WARNINGS advertencias menores (no críticas)${NC}"
    fi
    echo ""
    echo "🚀 Próximos pasos:"
    echo "   1. Ver estado del agente: cd agent && ./run.sh status"
    echo "   2. Iniciar servidor GUI: cd agent && ./run.sh gui-server"
    echo "   3. Compilar kernel: ./build.sh"
    echo "   4. Ejecutar F3-OS: ./run_safe.sh"
    exit 0
fi

