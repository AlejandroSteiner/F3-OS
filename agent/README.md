# F3-OS Governance Agent

Agente AI especializado que gobierna el desarrollo de F3-OS, manteniendo coherencia con el modelo F3.

## Arquitectura

El agente replica la estructura del F3 Core:

- **Code Analyzer** (CPU Thread): Analiza código propuesto
- **Context Manager** (RAM Thread): Mantiene contexto del proyecto
- **Synthesis Engine** (MEM Thread): Sintetiza propuestas y genera feedback
- **Governance Core** (F3 Core): Toma decisiones finales

## Instalación

```bash
cd agent
pip install -r requirements.txt
```

## Configuración

1. Copia `config/config.example.yaml` a `config/config.yaml`
2. Configura tus tokens de GitHub y API keys
3. Ajusta los parámetros según necesites

## Uso

### Método Recomendado: Script de Ejecución

```bash
cd agent
./run.sh [comando]
```

El script `run.sh`:
- ✅ Verifica que Python esté instalado
- ✅ Crea archivo de configuración si no existe
- ✅ Instala dependencias automáticamente si faltan
- ✅ Ejecuta el agente correctamente

### Comandos Disponibles

**Evaluar un PR específico:**
```bash
./run.sh evaluate-pr --pr 123
```

**Monitorear PRs automáticamente:**
```bash
./run.sh monitor
```

**Ver estado del agente:**
```bash
./run.sh status
```

**Ejecutar ciclo completo:**
```bash
./run.sh cycle
```

**Iniciar servidor GUI del asistente:**
```bash
./run.sh gui-server --port 8080
```

### Método Alternativo: Ejecución Directa

```bash
cd agent
python3 run_agent.py [comando]
```

Esto inicia un servidor HTTP que la GUI de F3-OS puede usar para comunicarse con el asistente.

## Documentación

Ver [AGENTE_GOBERNANTE.md](../AGENTE_GOBERNANTE.md) para la visión completa.

