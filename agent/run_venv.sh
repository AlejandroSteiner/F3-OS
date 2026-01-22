#!/bin/bash
# Script para ejecutar el agente usando entorno virtual

cd "$(dirname "$0")"

# Verificar que el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado"
    echo "Ejecuta primero: ./setup_venv.sh"
    exit 1
fi

# Activar entorno virtual y ejecutar
source venv/bin/activate
python3 run_agent.py "$@"




