#!/bin/bash
# Script para configurar entorno virtual para el agente

cd "$(dirname "$0")"

echo "🔧 Configurando entorno virtual para el Agente F3-OS..."
echo ""

# Crear entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Error: No se pudo crear el entorno virtual"
        echo "Asegúrate de tener python3-venv instalado:"
        echo "  sudo apt install python3-venv"
        exit 1
    fi
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Configuración completada"
    echo ""
    echo "Para usar el agente:"
    echo "  source venv/bin/activate"
    echo "  ./run.sh [comando]"
    echo ""
    echo "O ejecutar directamente:"
    echo "  ./run_venv.sh [comando]"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi


