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

# Verificar que las dependencias están instaladas
if ! python3 -c "import yaml, github, psutil" 2>/dev/null; then
    echo "⚠️  Advertencia: Dependencias no instaladas"
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ Dependencias instaladas"
    else
        echo "❌ Error instalando dependencias"
        echo "Intenta manualmente: pip3 install -r requirements.txt"
        exit 1
    fi
    echo ""
fi

# Ejecutar el agente
python3 run_agent.py "$@"

