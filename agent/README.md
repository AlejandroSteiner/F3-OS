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

### Evaluar un PR

```bash
python -m src.main evaluate-pr <PR_NUMBER>
```

### Monitorear PRs automáticamente

```bash
python -m src.main monitor
```

### Operar en ciclo de fases

```bash
python -m src.main cycle
```

## Documentación

Ver [AGENTE_GOBERNANTE.md](../AGENTE_GOBERNANTE.md) para la visión completa.

