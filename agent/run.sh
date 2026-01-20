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
    echo ""
    echo "Opciones para instalar dependencias:"
    echo ""
    echo "1. Usar entorno virtual (recomendado):"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    echo "   ./run.sh [comando]"
    echo ""
    echo "2. Instalar con pipx:"
    echo "   pipx install -r requirements.txt"
    echo ""
    echo "3. Instalar manualmente:"
    echo "   pip3 install --user -r requirements.txt"
    echo ""
    echo "4. Usar pip con --break-system-packages (no recomendado):"
    echo "   pip3 install --break-system-packages -r requirements.txt"
    echo ""
    read -p "¿Deseas intentar instalar con --user? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        pip3 install --user -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "✅ Dependencias instaladas"
        else
            echo "❌ Error instalando dependencias"
            echo "Por favor, instala manualmente usando una de las opciones arriba"
            exit 1
        fi
    else
        echo "Por favor, instala las dependencias manualmente antes de continuar"
        exit 1
    fi
    echo ""
fi

# Ejecutar el agente
python3 run_agent.py "$@"

