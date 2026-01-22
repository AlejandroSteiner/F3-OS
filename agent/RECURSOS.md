# Gestión de Recursos del Agente

## Límites de Recursos

El agente gobernante está diseñado para consumir **solo 15-20% de CPU** del sistema, asegurando que no sobrecargue el sistema mientras desarrolla F3-OS.

## Configuración

Los límites se configuran en `config/config.yaml`:

```yaml
resources:
  max_cpu_percent: 20.0      # Máximo 20% de CPU
  target_cpu_percent: 15.0   # Objetivo 15% de CPU
  check_interval: 1.0        # Verificar cada segundo
  sleep_duration: 0.1        # Pausa entre operaciones (100ms)
```

## Cómo Funciona

### 1. Monitoreo Continuo

El agente monitorea su propio uso de CPU en un thread separado:
- Verifica uso cada segundo
- Alerta si excede el límite máximo
- Registra estadísticas

### 2. Throttling Automático

Entre operaciones, el agente:
- Pausa automáticamente (`sleep_duration`)
- Verifica uso de CPU
- Aplica throttling adicional si es necesario
- Mantiene uso dentro del objetivo (15%)

### 3. Rate Limiting

Cada operación (evaluar PR, analizar código, etc.) está envuelta en un `ThrottledOperation`:
- Aplica pausa después de la operación
- Verifica que no exceda límites
- Ajusta dinámicamente según carga del sistema

## Ejemplo de Uso

```python
from src.resource_manager import ResourceManager, ThrottledOperation

resource_manager = ResourceManager(config)
resource_manager.start_monitoring()

# Operación con throttling automático
with ThrottledOperation(resource_manager):
    # Tu código aquí
    analyze_code()
    process_data()
    # Throttling se aplica automáticamente al salir
```

## Monitoreo

Para ver estadísticas de recursos:

```bash
python -m src.main status
```

Esto muestra:
- Uso actual de CPU
- Si está dentro de límites
- Si cumple el objetivo
- Memoria utilizada
- Número de operaciones

## Ajuste de Límites

Si necesitas ajustar los límites:

1. **Más permisivo** (más CPU):
   ```yaml
   max_cpu_percent: 25.0
   target_cpu_percent: 20.0
   ```

2. **Más restrictivo** (menos CPU):
   ```yaml
   max_cpu_percent: 15.0
   target_cpu_percent: 10.0
   sleep_duration: 0.2  # Pausas más largas
   ```

## Verificación

El agente verifica automáticamente:
- ✅ Uso dentro de límites
- ✅ Cumplimiento del objetivo
- ⚠️ Alertas si excede límites

## Impacto en Performance

Con estos límites:
- El agente procesa PRs más lentamente
- Pero no sobrecarga el sistema
- Permite que otros procesos usen CPU
- Ideal para ejecución continua en background

## Notas Técnicas

- Usa `psutil` para monitoreo de recursos
- Thread separado para monitoreo (no bloquea operaciones)
- Throttling se aplica automáticamente en todas las operaciones
- Configurable sin modificar código




