---
name: '[CONCEPTUAL] Cambio al Modelo F3'
about: Para cambios que afectan el núcleo conceptual de F3-OS
title: '[CONCEPTUAL] '
labels: conceptual, discussion-required
assignees: ''
---

## ⚠️ IMPORTANTE

Este template es para cambios que afectan el **núcleo sagrado** de F3-OS:
- F3 Core
- Los 3 hilos (CPU/RAM/MEM) - cambios estructurales
- El ciclo de fases
- La retroalimentación inversa

**NO uses este template para**:
- Bugs
- Features en áreas abiertas
- Mejoras de implementación

---

## ¿Qué componente del núcleo afecta?

- [ ] F3 Core (`kernel/src/f3/core.rs`)
- [ ] CPU Thread (`kernel/src/f3/cpu.rs`) - cambio estructural
- [ ] RAM Thread (`kernel/src/f3/ram.rs`) - cambio estructural
- [ ] MEM Thread (`kernel/src/f3/mem.rs`) - cambio estructural
- [ ] Ciclo de fases (SystemPhase)
- [ ] Retroalimentación inversa
- [ ] Otro (especificar)

---

## ¿Qué problema resuelve?

Describe el problema que este cambio resuelve. ¿Por qué es necesario modificar el núcleo?

---

## ¿Cuál es la propuesta?

Describe detalladamente qué quieres cambiar y cómo.

---

## ¿Cómo se alinea con el modelo F3?

Explica cómo este cambio:
- Se alinea con la filosofía "lógico → ilógico → síntesis → perfecto"
- Respeta el modelo de 3 hilos
- Mantiene la coherencia conceptual

---

## Alternativas consideradas

¿Consideraste otras soluciones? ¿Por qué esta es la mejor?

---

## Impacto esperado

- ¿Qué componentes se verán afectados?
- ¿Rompe compatibilidad con código existente?
- ¿Requiere cambios en documentación?

---

## Referencias

- [ ] He leído el [MANIFIESTO.md](../../MANIFIESTO.md)
- [ ] He leído [ARQUITECTURA_COMPLETA.md](../../ARQUITECTURA_COMPLETA.md)
- [ ] He leído [REGLAS_LOGICA.md](../../REGLAS_LOGICA.md)
- [ ] He leído [GOVERNANCE.md](../../GOVERNANCE.md)

---

**Recuerda**: Los cambios conceptuales requieren discusión profunda. No implementes código hasta que esta discusión se resuelva.

