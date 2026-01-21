# Guía de Contribución a F3-OS

## Antes de Contribuir

**Lee esto primero**: F3-OS no es un proyecto tradicional. Tiene reglas estrictas y un modelo conceptual que debe respetarse.

Si no has leído el [MANIFIESTO.md](MANIFIESTO.md), hazlo ahora. Si no entiendes el modelo F3, lee [ARQUITECTURA_COMPLETA.md](ARQUITECTURA_COMPLETA.md) y [REGLAS_LOGICA.md](REGLAS_LOGICA.md).

---

## Reglas Fundamentales

### 1. PRs Pequeños

**No envíes PRs masivos.**

- Un PR debe resolver un problema específico
- Máximo 200-300 líneas de cambios
- Si necesitas hacer cambios grandes, divídelos en múltiples PRs

**Por qué**: Facilita la revisión y mantiene el foco conceptual.

### 2. Cambios Conceptuales → Discusión Primero

**Si tu cambio afecta el modelo F3, discútelo antes de codificar.**

Esto incluye:
- Modificaciones al F3 Core
- Cambios en los 3 hilos (CPU/RAM/MEM)
- Alteraciones al ciclo de fases
- Cambios en la retroalimentación inversa

**Cómo discutir**:
1. Abre un Issue con la etiqueta `[CONCEPTUAL]`
2. Explica el problema que resuelve
3. Justifica por qué el cambio es necesario
4. Espera feedback antes de implementar

**Por qué**: El núcleo conceptual de F3-OS se custodia con cuidado. No todo se vota, pero todo se discute.

### 3. Nada de Features "Porque Sí"

**Cada cambio debe tener justificación.**

Antes de agregar una feature, pregúntate:
- ¿Resuelve un problema real del modelo F3?
- ¿Se alinea con la filosofía del proyecto?
- ¿Es necesaria ahora o puede esperar?

Si la respuesta es "sería cool tener esto", probablemente no deberías agregarlo.

**Por qué**: F3-OS no busca ser un "kitchen sink". Busca coherencia conceptual.

### 4. Respeta el Vocabulario del Proyecto

F3-OS tiene términos específicos:
- **Hilos** (no "threads" en el sentido tradicional)
- **Embudo** (Funnel, F3 Core)
- **Síntesis** (no "promedio" o "agregación")
- **Retroalimentación inversa** (enrollado inverso)
- **Fases**: Lógico, Ilógico, Síntesis, Perfecto

Usa estos términos correctamente. No los reemplaces con sinónimos genéricos.

**Por qué**: El vocabulario define el modelo mental. Cambiarlo confunde.

---

## Proceso de Contribución

### Paso 1: Fork y Clone

```bash
git clone https://github.com/tu-usuario/f3-os.git
cd f3-os
```

### Paso 2: Crea una Rama

```bash
git checkout -b feature/descripcion-corta
# o
git checkout -b fix/descripcion-corta
```

**Nomenclatura**:
- `feature/`: Nueva funcionalidad
- `fix/`: Corrección de bug
- `docs/`: Solo documentación
- `refactor/`: Refactorización sin cambio funcional

### Paso 3: Desarrolla

- Sigue las convenciones de código Rust
- Comenta código complejo
- Mantén PRs pequeños
- Prueba tus cambios (si es posible en el estado actual)

### Paso 4: Commit

```bash
git commit -m "tipo: descripción corta

Descripción más detallada si es necesario.

Refs: #issue-number"
```

**Tipos de commit**:
- `feat`: Nueva feature
- `fix`: Corrección de bug
- `docs`: Documentación
- `refactor`: Refactorización
- `test`: Tests
- `chore`: Mantenimiento

### Paso 5: Push y PR

```bash
git push origin feature/descripcion-corta
```

Luego abre un Pull Request en GitHub.

---

## Estructura del Pull Request

### Título

Debe ser claro y descriptivo:
- ✅ `feat: agregar medición de latencia en CPU Thread`
- ❌ `cambios`
- ❌ `mejoras varias`

### Descripción

**Obligatorio** incluir:

1. **¿Qué cambia?** (descripción breve)
2. **¿Por qué?** (justificación)
3. **¿Cómo?** (si es relevante)
4. **¿Afecta el modelo F3?** (sí/no y explicación)

### Ejemplo de Descripción

```markdown
## ¿Qué cambia?
Agrega medición de latencia promedio en el CPU Thread.

## ¿Por qué?
El CPU Thread actualmente solo reporta latencia del último ciclo. 
Necesitamos latencia promedio para mejor síntesis en el F3 Core.

## ¿Cómo?
Agrega campo `avg_latency` a `CpuFlow` y calcula promedio 
en cada ciclo.

## ¿Afecta el modelo F3?
No. Solo mejora la métrica que ya existe. No cambia el ciclo 
de fases ni la síntesis.
```

---

## El Núcleo Sagrado

**Estos componentes requieren discusión previa obligatoria:**

### F3 Core (`kernel/src/f3/core.rs`)
- Cambios a `process_funnel()`
- Modificaciones al ciclo de fases
- Cambios en `apply_feedback()`
- Alteraciones a la lógica de síntesis

### Los 3 Hilos
- `kernel/src/f3/cpu.rs` - CPU Thread
- `kernel/src/f3/ram.rs` - RAM Thread  
- `kernel/src/f3/mem.rs` - MEM Thread

**Cambios estructurales** (no solo mejoras de implementación) requieren Issue previo.

### El Ciclo de Fases
- Modificar `SystemPhase`
- Cambiar transiciones entre fases
- Alterar duración de fases
- Modificar lógica de entropía

---

## Código de Conducta

### Respeto

- Respeta las opiniones de otros
- Cuestiona ideas, no personas
- Sé constructivo en críticas

### Paciencia

- Las discusiones conceptuales pueden tomar tiempo
- No todos los PRs se aceptan
- Aprende de los rechazos

### Coherencia

- Mantén el foco en el modelo F3
- No intentes convertir F3-OS en otro proyecto
- Respeta la filosofía del proyecto

---

## Revisión de PRs

### Criterios de Aceptación

Un PR se acepta si:

1. ✅ Resuelve un problema real
2. ✅ Se alinea con el modelo F3
3. ✅ No rompe funcionalidad existente
4. ✅ Tiene justificación clara
5. ✅ Código es legible y mantenible
6. ✅ No afecta el núcleo sin discusión previa

### Criterios de Rechazo

Un PR se rechaza si:

1. ❌ Agrega features sin justificación
2. ❌ Modifica el núcleo sin discusión previa
3. ❌ Rompe el modelo conceptual
4. ❌ Es demasiado grande (divide en PRs más pequeños)
5. ❌ No sigue las convenciones del proyecto

---

## Preguntas Frecuentes

### ¿Puedo agregar un driver para X?

Depende. Si es necesario para el desarrollo del kernel y se alinea con el modelo F3, sí. Si es "porque sería útil", probablemente no.

**Pregunta primero** abriendo un Issue.

### ¿Puedo cambiar el ciclo de fases?

Solo si tienes una justificación conceptual sólida. **Discute primero** en un Issue con etiqueta `[CONCEPTUAL]`.

### ¿Puedo agregar compatibilidad POSIX?

No. F3-OS no busca compatibilidad POSIX. Es parte de su filosofía.

### ¿Cómo sé si mi cambio es "conceptual"?

Si afecta:
- F3 Core
- Los 3 hilos (estructura, no implementación)
- El ciclo de fases
- La retroalimentación inversa

Entonces es conceptual. **Discute primero**.

---

## Recursos

- [MANIFIESTO.md](MANIFIESTO.md) - Filosofía del proyecto
- [ARQUITECTURA_COMPLETA.md](ARQUITECTURA_COMPLETA.md) - Arquitectura técnica
- [REGLAS_LOGICA.md](REGLAS_LOGICA.md) - Explicación del ciclo de fases
- [README.md](README.md) - Documentación general

---

## Contacto

Si tienes dudas sobre si tu contribución es apropiada, abre un Issue con la etiqueta `[QUESTION]`.

**Recuerda**: F3-OS no es un proyecto tradicional. Respeta el modelo conceptual y contribuye con coherencia.

---

*Última actualización: 2025*


