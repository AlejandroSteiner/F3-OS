# Sistema de Reglas del Agente

## 🎯 Propósito

El sistema de reglas define **qué hacer, dónde parar, dónde buscar y cómo implementar** para que el agente pueda operar de forma autónoma y efectiva.

## 📋 Categorías de Reglas

### 1. QUÉ HACER (What to Do)

Define las acciones principales que el agente debe realizar:

- **Completar el Propósito del Proyecto**: Prioridad máxima
- **Mantener Coherencia con Modelo F3**: Todas las decisiones deben alinearse con F3
- **Aprender de Internet**: Aprender libremente para completar el proyecto

### 2. DÓNDE PARAR (Where to Stop)

Define cuándo el agente debe detenerse:

- **Núcleo Sagrado**: NUNCA modificar sin aprobación humana
- **Límites de Recursos**: Parar si se alcanzan límites (25% CPU, 8GB RAM, 50% red)
- **Incertidumbre**: Parar y consultar si confianza < 70%

### 3. DÓNDE BUSCAR (Where to Search)

Define dónde buscar información:

- **Conocimiento Local Primero**: Siempre buscar primero en el proyecto
- **Internet si Local Falla**: Buscar en internet si no hay información local
- **Núcleo Sagrado para Arquitectura**: Consultar MANIFIESTO.md, GOVERNANCE.md, etc.

### 4. CÓMO IMPLEMENTAR (How to Implement)

Define cómo implementar código:

- **Seguir Ciclo F3**: Lógico → Ilógico → Síntesis → Perfecto
- **Rust no_std**: Usar Rust con no_std para el kernel
- **Separación de Consultas**: GUI basada en separación de procesos
- **Con Testing**: Incluir pruebas cuando sea posible

### 5. LÍMITES DE RECURSOS (Resource Limits)

Define límites de recursos:

- **CPU**: Máximo 25% (6 núcleos, 12 hilos disponibles)
- **RAM**: Máximo 8GB
- **Red**: Máximo 50% de disponibilidad

### 6. PRIORIDADES (Priorities)

Define prioridades:

- **Completar Proyecto**: Prioridad máxima
- **Mantener Coherencia**: Alta prioridad
- **Consultas del Usuario**: Alta prioridad

## 🔧 Uso del Sistema de Reglas

### Cargar Reglas

Las reglas se cargan automáticamente al inicializar el `GovernanceCore`:

```python
from agent.src.agent_rules import AgentRulesSystem

rules = AgentRulesSystem(project_root="/path/to/f3-os")
```

### Consultar Reglas

```python
# Qué hacer
what_to_do = rules.get_what_to_do(context="implementation")

# Dónde parar
should_stop, stop_rule = rules.should_stop({
    'type': 'code_modification',
    'modified_files': ['kernel/src/f3/core.rs']
})

# Dónde buscar
search_strategy = rules.get_search_strategy("allocator", {
    'type': 'knowledge_gap',
    'local_search_failed': True
})

# Cómo implementar
implementation_guide = rules.get_how_to_implement(context="kernel_implementation")
```

### Límites de Recursos

```python
limits = rules.get_resource_limits()
# Returns: {
#     'max_cpu_percent': 25.0,
#     'max_ram_gb': 8.0,
#     'available_cores': 6,
#     'available_threads': 12,
#     'max_bandwidth_percent': 50.0
# }
```

## 📊 Reglas por Prioridad

Las reglas están ordenadas por prioridad (1-10, mayor = más importante):

1. **Prioridad 10**: Completar proyecto, mantener coherencia F3, límites de recursos
2. **Prioridad 9**: Parar en núcleo sagrado, buscar en núcleo sagrado, implementar con F3
3. **Prioridad 8**: Aprender de internet, buscar en internet, consultas del usuario
4. **Prioridad 7**: Parar en incertidumbre, implementar con testing

## 🔄 Integración con el Agente

El sistema de reglas está integrado en:

- **GovernanceCore**: Carga reglas al inicializar
- **ResourceManager**: Aplica límites de recursos desde reglas
- **Code Analyzer**: Verifica coherencia según reglas
- **Internet Learner**: Sigue estrategia de búsqueda según reglas

## ✅ Resultado

El agente ahora:

1. ✅ **Sabe qué hacer**: Completar proyecto, mantener coherencia, aprender
2. ✅ **Sabe dónde parar**: Núcleo sagrado, límites de recursos, incertidumbre
3. ✅ **Sabe dónde buscar**: Local primero, internet si falla, núcleo sagrado para arquitectura
4. ✅ **Sabe cómo implementar**: Ciclo F3, Rust no_std, separación de consultas, testing
5. ✅ **Respeta límites**: 25% CPU, 8GB RAM, 50% red, 6 núcleos, 12 hilos

---

**El agente está completamente configurado con reglas para operar de forma autónoma y efectiva.**







