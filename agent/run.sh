#!/bin/bash
# Script para ejecutar el Agente Gobernante F3-OS

cd "$(dirname "$0")"

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 no encontrado"
    echo "Instala Python 3.8 o superior"
    exit 1
fi

# Verificar que existe el archivo de configuración
if [ ! -f config/config.yaml ]; then
    echo "⚠️  Advertencia: config/config.yaml no encontrado"
    echo "Copiando config/config.example.yaml a config/config.yaml..."
    cp config/config.example.yaml config/config.yaml
    echo "✅ Archivo de configuración creado"
    echo "📝 Por favor, edita config/config.yaml y configura tu token de GitHub"
    echo ""
fi

# Verificar si existe entorno virtual
if [ -d "venv" ]; then
    # Usar entorno virtual si existe
    echo "🔌 Usando entorno virtual..."
    source venv/bin/activate
    PYTHON_CMD="python3"
elif python3 -c "import yaml, github, psutil" 2>/dev/null; then
    # Dependencias ya instaladas globalmente
    PYTHON_CMD="python3"
else
    # Crear y configurar entorno virtual automáticamente
    echo "📦 Creando entorno virtual automáticamente..."
    if ! python3 -m venv venv 2>/dev/null; then
        echo "❌ Error: No se pudo crear entorno virtual"
        echo "Instala python3-venv: sudo apt install python3-venv"
        exit 1
    fi
    
    source venv/bin/activate
    echo "📥 Instalando dependencias en entorno virtual..."
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Error instalando dependencias"
        exit 1
    fi
    
    echo "✅ Entorno virtual configurado"
    PYTHON_CMD="python3"
fi

# Ejecutar el agente
$PYTHON_CMD run_agent.py "$@"

