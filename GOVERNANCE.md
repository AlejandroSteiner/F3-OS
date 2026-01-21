# Governance de F3-OS

## Principio Fundamental

**F3-OS no es un proyecto democrático en todos sus aspectos.**

Algunos componentes son "sagrados" y requieren custodia especial. Esto no es autoritarismo, es protección del núcleo conceptual.

---

## Estructura de Gobierno

### Núcleo Sagrado (Core Team)

El **núcleo sagrado** de F3-OS está custodiado por el fundador y mantenedores principales. Este núcleo incluye:

1. **F3 Core** (`kernel/src/f3/core.rs`)
   - El embudo central y su lógica de síntesis
   - El ciclo de fases (Lógico → Ilógico → Síntesis → Perfecto)
   - La retroalimentación inversa

2. **Los 3 Hilos Estructurales**
   - CPU Thread (`kernel/src/f3/cpu.rs`)
   - RAM Thread (`kernel/src/f3/ram.rs`)
   - MEM Thread (`kernel/src/f3/mem.rs`)

3. **El Modelo Conceptual**
   - La filosofía "lógico → ilógico → síntesis → perfecto"
   - El vocabulario del proyecto
   - Las reglas fundamentales

**Cambios al núcleo sagrado**:
- Requieren discusión previa obligatoria (Issue con etiqueta `[CONCEPTUAL]`)
- Deben tener justificación sólida
- No se votan, se evalúan por coherencia conceptual
- El mantenedor principal tiene veto final

### Áreas Abiertas

Estas áreas son más flexibles y aceptan contribuciones con menos restricciones:

- Drivers (excepto si afectan el modelo F3)
- Herramientas de build
- Documentación (excepto el manifiesto)
- Scripts de utilidad
- Tests

**Cambios en áreas abiertas**:
- Siguen el proceso normal de PR
- Requieren revisión pero no discusión previa obligatoria
- Se evalúan por calidad técnica y alineación con el proyecto

---

## Proceso de Decisión

### Niveles de Decisión

#### Nivel 1: Cambios Técnicos Menores
- **Ejemplos**: Fixes de bugs, mejoras de implementación, refactorizaciones
- **Proceso**: PR normal → Revisión → Merge
- **Tiempo**: 1-3 días

#### Nivel 2: Cambios Técnicos Mayores
- **Ejemplos**: Nuevos drivers, mejoras significativas de performance
- **Proceso**: Issue de discusión → PR → Revisión extendida → Merge
- **Tiempo**: 1-2 semanas

#### Nivel 3: Cambios Conceptuales
- **Ejemplos**: Modificaciones al F3 Core, cambios en el ciclo de fases
- **Proceso**: Issue `[CONCEPTUAL]` → Discusión profunda → Justificación → PR → Revisión exhaustiva → Decisión del mantenedor
- **Tiempo**: 2-4 semanas (o más si es necesario)

### Criterios de Decisión

Un cambio se acepta si:

1. ✅ **Coherencia conceptual**: Se alinea con el modelo F3
2. ✅ **Justificación sólida**: Resuelve un problema real
3. ✅ **Calidad técnica**: Código limpio y mantenible
4. ✅ **No rompe filosofía**: Respeta los principios del manifiesto

Un cambio se rechaza si:

1. ❌ **Rompe el modelo**: Va contra la filosofía F3
2. ❌ **Sin justificación**: "Sería cool" no es suficiente
3. ❌ **Incompatible**: Busca convertir F3-OS en otro proyecto
4. ❌ **Prematuro**: No es necesario ahora

---

## Roles y Responsabilidades

### Mantenedor Principal (Founder)

**Responsabilidades**:
- Custodiar el núcleo sagrado
- Decisión final en cambios conceptuales
- Mantener coherencia del proyecto
- Revisar PRs críticos

**Poderes**:
- Veto en cambios al núcleo sagrado
- Aceptar/rechazar PRs sin consenso
- Modificar el manifiesto y governance

### Mantenedores (Maintainers)

**Responsabilidades**:
- Revisar PRs
- Mantener calidad del código
- Guiar a contribuidores
- Proponer mejoras

**Poderes**:
- Aprobar PRs en áreas abiertas
- Sugerir cambios conceptuales
- Etiquetar Issues

### Contribuidores (Contributors)

**Responsabilidades**:
- Seguir las reglas de contribución
- Respetar el modelo F3
- Mantener calidad en sus PRs

**Poderes**:
- Abrir Issues y PRs
- Participar en discusiones
- Proponer mejoras

---

## Resolución de Conflictos

### Si hay desacuerdo:

1. **Discusión en Issue**: Abre un Issue con etiqueta `[DISCUSSION]`
2. **Argumentos técnicos**: Presenta justificación basada en el modelo F3
3. **Tiempo de reflexión**: No se toman decisiones apresuradas
4. **Decisión final**: El mantenedor principal decide si no hay consenso

### Principios de resolución:

- **Coherencia > Consenso**: Mejor una decisión coherente que un compromiso que diluya el proyecto
- **Modelo F3 > Opiniones personales**: Las decisiones se basan en el modelo, no en preferencias
- **Respeto mutuo**: Se cuestionan ideas, no personas

---

## Transparencia

### Lo que es público:

- ✅ Todas las decisiones se documentan en Issues/PRs
- ✅ Las razones de rechazo se explican claramente
- ✅ El proceso es transparente

### Lo que no es público:

- ❌ Discusiones privadas (si las hay) se resumen públicamente
- ❌ No hay "backroom deals"

---

## Evolución del Governance

Este documento puede evolucionar, pero:

- Cualquier cambio requiere discusión pública
- El núcleo sagrado siempre será custodiado
- Los principios fundamentales no cambian sin justificación excepcional

---

## Preguntas Frecuentes

### ¿Por qué no es completamente democrático?

Porque F3-OS tiene un modelo conceptual específico. La democracia sin límites diluye la visión. Linux funciona así (Linus tiene veto). Rust funciona así (el core team decide). F3-OS también.

### ¿Puedo convertirme en mantenedor?

Con el tiempo, si demuestras:
- Comprensión profunda del modelo F3
- Contribuciones consistentes y de calidad
- Respeto por la filosofía del proyecto

Pero no hay proceso formal aún. El proyecto es joven.

### ¿Qué pasa si no estoy de acuerdo con una decisión?

Puedes:
1. Discutir en el Issue correspondiente
2. Presentar argumentos técnicos
3. Fork el proyecto (es código abierto)

Pero el mantenedor principal tiene la decisión final en el núcleo sagrado.

---

## Conclusión

**F3-OS no es un experimento social. Es un experimento de sistema operativo cognitivo.**

El governance protege el núcleo conceptual mientras permite evolución en áreas abiertas. Esto no es autoritarismo, es coherencia.

Si esto no te parece bien, F3-OS probablemente no es para ti. Y eso está bien.

---

*Última actualización: 2025*


