#!/usr/bin/env python3
"""
Script de ejecución para el Agente Gobernante F3-OS
Ejecuta el agente desde el directorio correcto
"""

import sys
from pathlib import Path

# Agregar el directorio agent al path
agent_dir = Path(__file__).parent
sys.path.insert(0, str(agent_dir))

# Importar y ejecutar main
from src.main import main

if __name__ == '__main__':
    main()

