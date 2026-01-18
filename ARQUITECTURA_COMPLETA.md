# Arquitectura Completa de F3-OS

## Mapa Conceptual del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     F3-OS KERNEL                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              ENTRY POINT (_start)                     │   │
│  │  kernel/src/main.rs                                   │   │
│  │  - VGA initialization                                 │   │
│  │  - F3 Core initialization                             │   │
│  │  - Main loop                                          │   │
│  └──────────────────────────────────────────────────────┘   │
│                          │                                    │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              F3 CORE (Núcleo Central)                 │   │
│  │  kernel/src/f3/core.rs                                │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │  SystemPhase: Logical → Illogical →          │    │   │
│  │  │              Synthesis → Perfect              │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  │                                                       │   │
│  │  - process_funnel()                                  │   │
│  │  - introduce_illogical_behavior()                    │   │
│  │  - calculate_perfection_score()                      │   │
│  │  - apply_feedback()                                  │   │
│  └──────────────────────────────────────────────────────┘   │
│         │              │              │                      │
│         ▼              ▼              ▼                      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                  │
│  │ CPU TL  │   │ RAM TL  │   │ MEM TL  │                  │
│  │ (Hilo 1)│   │ (Hilo 2)│   │ (Hilo 3)│                  │
│  └─────────┘   └─────────┘   └─────────┘                  │
│       │              │              │                      │
│       └──────────────┼──────────────┘                      │
│                      ▼                                      │
│            [EMBUDO DE SÍNTESIS]                             │
│                      ▼                                      │
│            [RETROALIMENTACIÓN]                              │
│                      │                                      │
│                      ▼                                      │
│         [RE-ESCRIBE REGLAS]                                 │
│                      │                                      │
│                      ▼                                      │
│            [NUEVO CICLO]                                    │
└─────────────────────────────────────────────────────────────┘
```

## Los 3 Hilos Fundamentales

### 1. CPU Thread (`kernel/src/f3/cpu.rs`)
**Responsabilidad**: Ejecución y medición

```rust
CpuFlow {
    task_id: u64,
    cycles_used: u64,
    last_latency: u32,
    active: bool,
}
```

**Funciones**:
- `init()`: Inicializa el hilo CPU
- `record_execution()`: Registra ejecución de tareas
- `get_flow()`: Obtiene estado actual
- `reset()`: Resetea métricas

**Ciclo**:
1. Recibe tareas a ejecutar
2. Mide ciclos y latencia
3. Reporta al F3 Core

---

### 2. RAM Thread (`kernel/src/f3/ram.rs`)
**Responsabilidad**: Contexto y presión de memoria

```rust
RamFlow {
    task_id: u64,
    memory_used: usize,
    pressure: u8,  // 0-255
    active: bool,
}
```

**Funciones**:
- `init()`: Inicializa el hilo RAM
- `record_usage()`: Registra uso de memoria
- `get_flow()`: Obtiene estado actual
- `reset()`: Resetea métricas

**Ciclo**:
1. Monitorea uso de memoria
2. Calcula presión (0-255)
3. Decide qué mantener/descartar
4. Reporta al F3 Core

---

### 3. MEM Thread (`kernel/src/f3/mem.rs`)
**Responsabilidad**: Síntesis y detección de patrones

```rust
MemFlow {
    task_id: u64,
    success_score: i8,  // -128 a 127
    anomaly: bool,
    active: bool,
}
```

**Funciones**:
- `init()`: Inicializa el sintetizador
- `synthesize()`: Sintetiza métricas de CPU y RAM
- `get_flow()`: Obtiene estado actual
- `reset()`: Resetea métricas

**Ciclo**:
1. Recibe métricas de CPU y RAM
2. Sintetiza en un score único
3. Detecta anomalías
4. Genera feedback

---

## F3 Core (El Embudo)

### Estructura (`kernel/src/f3/core.rs`)

```rust
F3State {
    hash: u64,           // Hash de estado
    priority_bias: i8,   // Sesgo de prioridad
    memory_bias: i8,     // Sesgo de memoria
    cycle_count: u64,    // Contador de ciclos
    phase: SystemPhase,  // Fase actual
    entropy: u8,         // Medida de caos
    perfection_score: i16, // Score de perfección
}
```

### Las 4 Fases del Sistema

#### 1. Fase LÓGICO (Logical)
- **Estado**: Ordenado, predecible
- **Entropía**: 0 (sin caos)
- **Duración**: ~50 ciclos
- **Transición**: Cuando necesita explorar

#### 2. Fase ILÓGICO (Illogical)
- **Estado**: Caos exploratorio
- **Entropía**: 100-255 (caos creciente)
- **Duración**: Hasta entropía > 200
- **Acción**: Desordena intencionalmente
- **Transición**: Cuando hay suficiente caos para sintetizar

#### 3. Fase SÍNTESIS (Synthesis)
- **Estado**: Concentración del embudo
- **Entropía**: Decrece (orden emerge)
- **Acción**: Sintetiza lo aprendido
- **Transición**: Cuando entropía < 50

#### 4. Fase PERFECTO (Perfect)
- **Estado**: Nuevo orden optimizado
- **Perfección**: Mayor que el lógico inicial
- **Acción**: Aplica feedback optimizado
- **Transición**: Ciclo completo → vuelve a LÓGICO mejorado

---

## Ciclo Completo del Sistema

```
[INICIO]
    │
    ▼
[FASE LÓGICO]
    │  Estructura ordenada
    │  Entropía = 0
    │  Comportamiento predecible
    │
    ▼ [ciclo % 50 == 0]
[FASE ILÓGICO]
    │  Introduce caos
    │  Entropía crece
    │  Explora soluciones
    │
    ▼ [entropía > 200]
[FASE SÍNTESIS]
    │  Embudo concentra
    │  Sintetiza métricas
    │  Entropía decrece
    │  Orden emerge
    │
    ▼ [entropía < 50]
[FASE PERFECTO]
    │  Nuevo orden superior
    │  Aplica feedback
    │  Perfección > inicial
    │
    ▼ [ciclo % 200 == 0]
[VUELVE A LÓGICO]
    │  Pero con mejor estado
    │
    └─► [CICLO CONTINÚA]
```

---

## Estructura de Archivos

```
f3-os/
├── kernel/                  # ⭐ CÓDIGO PROPIO DE F3-OS
│   ├── src/
│   │   ├── main.rs          # Entry point, loop principal
│   │   ├── vga.rs           # Driver VGA (salida texto)
│   │   ├── boot.rs          # Multiboot header
│   │   ├── arch/
│   │   │   ├── mod.rs       # Módulo de arquitectura
│   │   │   └── x86_64.rs    # Específico x86_64
│   │   └── f3/              # ⭐ NÚCLEO F3 (propio)
│   │       ├── mod.rs       # Módulo F3
│   │       ├── cpu.rs       # CPU Thread ⭐
│   │       ├── ram.rs       # RAM Thread ⭐
│   │       ├── mem.rs       # MEM Thread (Synthesizer) ⭐
│   │       └── core.rs      # F3 Core (embudo) ⭐
│   ├── linker.ld            # Linker script
│   └── Cargo.toml           # Configuración Rust
├── boot/
│   └── limine.cfg           # Config bootloader externo (Limine)
├── limine/                  # ⚠️ EXTERNO - Bootloader de terceros
│   └── ...                  # (No es parte de F3-OS)
├── build.sh                 # Script de compilación
├── run.sh                   # Script de ejecución QEMU
├── x86_64-unknown-none.json # Target Rust personalizado
└── README.md                # Documentación principal
```

**Nota**: `limine/` es un subdirectorio externo (bootloader de terceros), no parte del código de F3-OS.

---

## Flujo de Datos

### 1. Entrada (Input)
- Los 3 hilos reciben eventos/métricas
- CPU: Ciclos, latencia
- RAM: Memoria, presión
- MEM: Patrones, anomalías

### 2. Procesamiento (Processing)
```
[CPU Flow] ──┐
[RAM Flow] ──┼──► [F3 Core] ──► [Síntesis]
[MEM Flow] ──┘                      │
                                    ▼
                            [Hash de Estado]
                                    │
                                    ▼
                            [Feedback Bias]
```

### 3. Salida (Output)
- Prioridad ajustada
- Límites de memoria ajustados
- Reglas re-escritas
- Retroalimentación aplicada

---

## Conceptos Clave

### 1. Embudo (Funnel)
**Definición**: Concentración de múltiples flujos en un solo punto

**Implementación**: `process_funnel()` en `core.rs`

**Propósito**: 
- Recibe 3 flujos independientes
- Los concentra en un punto (F3 Core)
- Sintetiza en un estado único

### 2. Síntesis (Synthesis)
**Definición**: Combinación inteligente de múltiples métricas

**Implementación**: `synthesize()` en `mem.rs`

**Propósito**:
- No es un promedio simple
- Analiza correlaciones
- Genera score único

### 3. Retroalimentación (Feedback)
**Definición**: El resultado re-escribe las reglas

**Implementación**: `apply_feedback()` en `core.rs`

**Propósito**:
- Ajusta prioridades dinámicamente
- Modifica límites de memoria
- Sistema aprende y mejora

### 4. Enrollado Inverso (Reverse Winding)
**Definición**: El final del ciclo ajusta el principio

**Implementación**: Ciclo completo de 4 fases

**Propósito**:
- Estado final re-escribe estado inicial
- Sistema evoluciona cada ciclo
- Mejora progresiva

---

## Reglas Fundamentales

### Regla #1: Lógico → Ilógico → Síntesis → Perfecto

**Cada ciclo pasa por estas 4 fases obligatoriamente.**

No se puede saltar fases. El orden es estricto.

### Regla #2: El Embudo Nunca Se Detiene

**F3 Core procesa continuamente.**

Cada ciclo ejecuta `process_funnel()`, sin excepción.

### Regla #3: Los 3 Hilos Son Estructurales

**No son procesos normales.**

Son roles arquitectónicos que definen la estructura del sistema.

### Regla #4: La Síntesis Es Obligatoria

**No hay decisiones basadas en una sola métrica.**

Todas las decisiones pasan por síntesis en el F3 Core.

### Regla #5: La Retroalimentación Es Inversa

**El final ajusta el principio.**

El feedback viaja en sentido inverso al ciclo siguiente.

---

## Estado Actual del Sistema

### ✅ Implementado

- [x] Entry point (`_start`)
- [x] VGA driver (salida texto)
- [x] CPU Thread (medición de ciclos/latencia)
- [x] RAM Thread (monitoreo de memoria)
- [x] MEM Thread (síntesis de métricas)
- [x] F3 Core (embudo y retroalimentación)
- [x] 4 fases del ciclo (Logical → Illogical → Synthesis → Perfect)
- [x] Multiboot header (para QEMU)
- [x] Compilación completa del kernel
- [x] Scripts de build y ejecución
- [x] Documentación completa de arquitectura

### 🚧 Pendiente

- [ ] Boot correcto en QEMU (requiere bootloader Limine o corrección de Multiboot)
- [ ] Interrupciones y timer
- [ ] Scheduler F3 real
- [ ] Gestión de memoria (paging, allocator)
- [ ] Tareas y procesos
- [ ] Syscalls
- [ ] Red (opcional)

### 📋 Nota sobre Boot

El kernel está compilado correctamente pero QEMU requiere un bootloader (Limine) para bootear kernels bare metal personalizados. Usa `./create_iso.sh` para crear una ISO booteable.

---

## Métricas y Estado

### Variables de Estado Global

```rust
F3_STATE: F3State {
    hash: u64,              // Identificador único de estado
    priority_bias: i8,      // Ajuste de prioridades
    memory_bias: i8,        // Ajuste de memoria
    cycle_count: u64,       // Contador global de ciclos
    phase: SystemPhase,     // Fase actual del ciclo
    entropy: u8,            // 0-255: medida de caos
    perfection_score: i16,  // -32768 a 32767: calidad
}
```

### Flujos de los Hilos

```rust
CPU_FLOW: CpuFlow { ... }
RAM_FLOW: RamFlow { ... }
MEM_FLOW: MemFlow { ... }
```

---

## Conclusión

**F3-OS es un sistema operativo experimental basado en:**

1. **3 Hilos Estructurales** (CPU, RAM, MEM) ⭐ **PROPIO**
2. **Embudo de Síntesis** (F3 Core) ⭐ **PROPIO**
3. **Retroalimentación Inversa** (enrollado inverso) ⭐ **PROPIO**
4. **Ciclo de 4 Fases** (Lógico → Ilógico → Síntesis → Perfecto) ⭐ **PROPIO**

**La innovación está en el modelo, no en las partes individuales.**

---

## Componentes Externos vs Propios

### ⭐ Propio de F3-OS (la innovación):

- **Kernel completo** (`kernel/src/`)
- **F3 Core** (embudo de síntesis)
- **3 Hilos estructurales** (CPU, RAM, MEM)
- **Sistema de fases** (Lógico → Ilógico → Síntesis → Perfecto)
- **Arquitectura de retroalimentación**

### ⚠️ Externo (herramientas):

- **Limine**: Bootloader externo (solo para cargar el kernel)
- **Rust**: Lenguaje de programación
- **QEMU**: Emulador para pruebas
- **GNU Make**: Sistema de build

**Limine es solo la herramienta que carga F3-OS, no es parte de la innovación.**

La innovación está en **cómo funciona F3-OS una vez que está corriendo**, no en cómo se carga.

