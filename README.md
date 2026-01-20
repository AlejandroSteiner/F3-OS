# F3-OS: Funnel / Fiber / Feedback Operating System

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Rust](https://img.shields.io/badge/Rust-1.70+-orange.svg)](https://www.rust-lang.org/)
[![Architecture](https://img.shields.io/badge/Architecture-x86__64-green.svg)](https://en.wikipedia.org/wiki/X86-64)

**F3-OS** es un sistema operativo experimental de código abierto basado en un modelo innovador de **3 hilos (threads) fundamentales** que se fusionan en un **embudo (funnel)** central, creando un flujo de retroalimentación adaptativo que gobierna la planificación, memoria y ejecución del sistema.

> **⚠️ IMPORTANTE**: Lee el [MANIFIESTO.md](MANIFIESTO.md) antes de contribuir. F3-OS no es un sistema operativo tradicional. Es un experimento cognitivo a nivel kernel con reglas y filosofía específicas.

## 🎯 Concepto Principal

F3-OS está inspirado en la metáfora gráfica de **"enrollar 3 hilos de fibra óptica en su cartucho en reversa"**, lo cual se traduce técnicamente en:

- **3 Hilos Fundamentales**: CPU (Executor), RAM (Context Keeper), MEM (Synthesizer)
- **Embudo Central (F3 Core)**: Recibe, comprime y sintetiza flujos de los 3 hilos
- **Retropropagación Inversa**: El estado final reescribe decisiones anteriores
- **Ciclo Adaptativo**: Lógico → Ilógico → Síntesis → Perfecto

## 🏗️ Arquitectura

### 3 Hilos Fundamentales

1. **CPU Thread (Executor)**
   - Ejecuta tareas
   - Mide ciclos reales
   - Reporta latencias

2. **RAM Thread (Context Keeper)**
   - Mantiene estados parciales
   - Crea snapshots comprimidos
   - Decide qué descartar

3. **MEM Thread (Synthesizer)**
   - Memoria semántica
   - Resume patrones y resultados
   - Proporciona retroalimentación

### F3 Core (Funnel)

El corazón del sistema que:
- Recibe flujos de los 3 hilos
- Comprime estado
- Genera retroalimentación estructural
- Modifica planificación y memoria dinámicamente

### Ciclo de Fases del Sistema

F3-OS opera en un ciclo de 4 fases:

1. **LÓGICO**: Ordenado, predecible, baja entropía
2. **ILÓGICO**: Desorden intencional, exploración, alta entropía
3. **SÍNTESIS**: El embudo concentra, reorganiza, entropía disminuye
4. **PERFECTO**: Estado optimizado, aplica retroalimentación refinada

Este ciclo se repite continuamente, mejorando el sistema en cada iteración.

## 📁 Estructura del Proyecto

```
f3-os/
├── kernel/                 # Código fuente del kernel
│   ├── src/
│   │   ├── main.rs        # Punto de entrada del kernel
│   │   ├── vga.rs         # Driver de VGA para salida de texto
│   │   ├── f3/            # Módulos F3 Core
│   │   │   ├── mod.rs
│   │   │   ├── cpu.rs     # CPU Thread
│   │   │   ├── ram.rs     # RAM Thread
│   │   │   ├── mem.rs     # MEM Thread
│   │   │   └── core.rs    # F3 Core (Funnel)
│   │   ├── arch/          # Código específico de arquitectura
│   │   │   └── x86_64.rs
│   │   └── boot.rs        # Multiboot header
│   ├── linker.ld          # Script del linker
│   └── Cargo.toml         # Configuración de Rust
├── build.sh               # Script para compilar el kernel
├── run.sh                 # Script para ejecutar en QEMU (boot directo)
├── create_grub_iso.sh     # Script para crear ISO booteable con GRUB
├── run_iso.sh             # Script para ejecutar ISO en QEMU
└── README.md              # Este archivo
```

## 🚀 Inicio Rápido

### Requisitos

- **Rust** (nightly): `rustup toolchain install nightly`
- **QEMU**: `sudo apt install -y qemu-system-x86`
- **GRUB**: `sudo apt install -y grub-pc-bin grub-common xorriso mtools`
- **LLVM/LLD**: `sudo apt install -y llvm lld`

O instala todo de una vez:
```bash
./INSTALAR_DEPENDENCIAS.sh
```

### Compilar

```bash
./build.sh
```

Esto generará `kernel.bin` en la raíz del proyecto.

### Ejecutar

#### Opción 1: Boot Directo (no requiere ISO)
```bash
./run.sh
```

#### Opción 2: ISO Booteable (más compatible)
```bash
# Crear ISO
./create_grub_iso.sh

# Ejecutar ISO
./run_iso.sh
```

## 📖 Documentación

### Documentos Esenciales (Lee Primero)

- **[MANIFIESTO.md](MANIFIESTO.md)**: ⭐ **OBLIGATORIO** - Qué es y qué NO es F3-OS
- **[CONTRIBUTING.md](CONTRIBUTING.md)**: ⭐ **OBLIGATORIO** - Reglas de contribución
- **[GOVERNANCE.md](GOVERNANCE.md)**: Estructura de gobierno y núcleo sagrado
- **[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)**: Código de conducta de la comunidad
- **[ARQUITECTURA_COMPLETA.md](ARQUITECTURA_COMPLETA.md)**: Documentación completa de la arquitectura
- **[REGLAS_LOGICA.md](REGLAS_LOGICA.md)**: Explicación del ciclo "Lógico → Ilógico → Síntesis → Perfecto"

### Documentos Técnicos

- **[INNOVACION_Y_VALOR.md](INNOVACION_Y_VALOR.md)**: Innovación y valor del sistema
- **[GUIA_PRUEBAS_SEGURAS.md](GUIA_PRUEBAS_SEGURAS.md)**: Guía para pruebas seguras en QEMU
- **[DEBUG_GRUB.md](DEBUG_GRUB.md)**: Troubleshooting de problemas con GRUB
- **[SOLUCION_FINAL.md](SOLUCION_FINAL.md)**: Soluciones a problemas comunes

### Estado Actual

**Versión**: 0.1.0 (Desarrollo inicial)

**Estado**: ✅ Kernel funcional básico, sistema de fases implementado, arranque en QEMU (con algunas limitaciones)

**Funcionalidades Implementadas**:
- ✅ Kernel básico en Rust (`#![no_std]`)
- ✅ Driver VGA para salida de texto
- ✅ Sistema F3 Core con 3 hilos
- ✅ Ciclo de fases: Lógico → Ilógico → Síntesis → Perfecto
- ✅ Multiboot header para bootloaders
- ✅ Scripts de build y ejecución

**Problemas Conocidos**:
- ⚠️ GRUB puede tener problemas detectando el Multiboot header (usar opciones de debugging)
- ⚠️ Sistema se congela al intentar arrancar desde ISO (problema de bootloader)

**Próximos Pasos**:
- [ ] Mejorar detección de Multiboot header en GRUB
- [ ] Implementar scheduler adaptativo
- [ ] Sistema de memoria dinámico
- [ ] Drivers básicos (teclado, disco)
- [ ] Sistema de archivos simple

## 🔬 Desarrollo

### Compilar el Kernel

```bash
cd /home/ktzchen/Documentos/f3-os
./build.sh
```

El kernel se compila para el target `x86_64-unknown-none` usando Rust nightly y `build-std`.

### Ejecutar en QEMU

```bash
# Boot directo (requiere Multiboot header)
./run.sh

# Desde ISO (requiere crear ISO primero)
./create_grub_iso.sh
./run_iso.sh
```

### Debugging

Para debugging en QEMU:

```bash
qemu-system-x86_64 \
  -cdrom f3os.iso \
  -display gtk \
  -m 256M \
  -no-reboot \
  -serial stdio \
  -s -S  # Para conectar con GDB
```

## 📝 Regla Fundamental del Sistema

**"Lógico pero ilógico en su estructura hasta volver a ser lógico y perfecto de nuevo"**

Esta regla se implementa como el ciclo de fases del sistema:
1. Empieza ordenado y predecible (LÓGICO)
2. Introduce desorden intencional para explorar (ILÓGICO)
3. El embudo sintetiza y reorganiza (SÍNTESIS)
4. El sistema se optimiza y vuelve al orden mejorado (PERFECTO)

Este ciclo se repite continuamente, mejorando el sistema en cada iteración.

## 🤝 Contribuir

**Antes de contribuir, lee**:
- [MANIFIESTO.md](MANIFIESTO.md) - Filosofía y principios del proyecto
- [CONTRIBUTING.md](CONTRIBUTING.md) - Reglas estrictas de contribución

F3-OS tiene reglas específicas:
- PRs pequeños (máximo 200-300 líneas)
- Cambios conceptuales requieren discusión previa
- Nada de features "porque sí"
- Respeta el vocabulario y modelo F3

**No contribuyas si**:
- Buscas un proyecto "fácil" o tradicional
- No estás dispuesto a entender el modelo conceptual
- Quieres agregar compatibilidad POSIX o features genéricas

**Sí contribuye si**:
- Te interesa experimentación en arquitectura de sistemas
- Entiendes y respetas el modelo F3
- Estás dispuesto a cuestionar y ser cuestionado

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para el proceso completo.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia GPL-3.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**AlejandroSteiner**

## 🙏 Agradecimientos

- Rust community por el excelente lenguaje
- QEMU project por el emulador
- GRUB project por el bootloader
- Comunidad de OSDev por recursos y conocimiento

## 📚 Recursos

- [OSDev Wiki](https://wiki.osdev.org/)
- [Writing an OS in Rust](https://os.phil-opp.com/)
- [Rust Embedded Book](https://docs.rust-embedded.org/book/)

---

## ⚠️ Advertencias Importantes

### Lo que F3-OS NO es:

- ❌ **NO es un sistema operativo de producción** - Es experimental
- ❌ **NO busca compatibilidad POSIX** - Tiene su propio modelo
- ❌ **NO es un proyecto tradicional** - Tiene reglas y filosofía específicas
- ❌ **NO es para todos** - Requiere entender el modelo conceptual

### Lo que F3-OS SÍ es:

- ✅ **Es un experimento cognitivo a nivel kernel**
- ✅ **Es código abierto** (GPL-3.0)
- ✅ **Es un laboratorio de ideas** sobre retroalimentación adaptativa
- ✅ **Es para quienes buscan experimentación** en arquitectura de sistemas

**Lee el [MANIFIESTO.md](MANIFIESTO.md) para entender completamente qué es F3-OS.**

---

**⚠️ Advertencia**: Este es un proyecto experimental. No use en producción. Úsalo bajo tu propio riesgo.

**⭐ Si te gusta este proyecto, considera darle una estrella en GitHub!**

