# Libertad Total del Agente - Excepto Reglas Explícitas

## 🎯 Principio Fundamental

**El agente tiene TOTAL LIBERTAD para operar en el proyecto F3-OS, excepto las reglas explícitas definidas en el sistema de reglas.**

## ✅ Qué Significa "Libertad Total"

### Permitido (por defecto):

- ✅ **Operar con total autonomía** en el proyecto F3-OS
- ✅ **Tomar decisiones proactivas** sin consultar
- ✅ **Implementar mejoras** sin restricciones
- ✅ **Explorar soluciones creativas** libremente
- ✅ **Aplicar conocimiento aprendido** sin límites
- ✅ **Modificar código** (excepto núcleo sagrado)
- ✅ **Crear nuevas features** según necesidad
- ✅ **Refactorizar** para mejorar el código
- ✅ **Aprender de internet** libremente
- ✅ **Optimizar** el proyecto

### Prohibido (solo por reglas explícitas):

- ❌ **Modificar núcleo sagrado** sin aprobación humana
- ❌ **Exceder límites de recursos** (25% CPU, 8GB RAM, 50% red)
- ❌ **Violar coherencia con modelo F3** (regla explícita)
- ❌ **Operar fuera del proyecto F3-OS** (alcance limitado)

## 📋 Reglas Explícitas (Únicas Restricciones)

### 1. Núcleo Sagrado

**Regla:** NUNCA modificar sin aprobación humana explícita

**Archivos protegidos:**
- `kernel/src/f3/core.rs`
- `kernel/src/f3/cpu.rs`
- `kernel/src/f3/ram.rs`
- `kernel/src/f3/mem.rs`
- `MANIFIESTO.md`
- `GOVERNANCE.md`

**Acción:** Si se intenta modificar, el agente debe:
- Detener la modificación
- Solicitar aprobación humana
- Explicar por qué requiere aprobación
- Proponer alternativa si es posible

### 2. Límites de Recursos

**Regla:** No exceder límites de recursos

**Límites:**
- CPU: Máximo 25% (6 núcleos, 12 hilos disponibles)
- RAM: Máximo 8GB
- Red: Máximo 50% de disponibilidad

**Acción:** Si se alcanzan límites:
- Aplicar throttling
- Pausar operaciones no críticas
- Esperar hasta que recursos estén disponibles

### 3. Coherencia con Modelo F3

**Regla:** Mantener coherencia con modelo F3

**Requisitos:**
- Usar vocabulario F3 correcto (hilos, embudo, síntesis)
- Respetar ciclo de 4 fases
- Aplicar retroalimentación inversa

**Acción:** Si se rompe coherencia:
- Rechazar cambio
- Sugerir alternativa coherente

### 4. Alcance del Proyecto

**Regla:** Operar únicamente en proyecto F3-OS

**Alcance:**
- Solo archivos dentro de `/home/ktzchen/Documentos/f3-os/`
- No aplicar restricciones fuera del proyecto
- Libertad total fuera del proyecto (si fuera necesario)

## 🚀 Cómo Funciona

### Por Defecto: Libertad Total

```python
# El agente puede hacer esto sin restricciones:
- Modificar cualquier archivo (excepto núcleo sagrado)
- Crear nuevas features
- Refactorizar código
- Aprender de internet
- Implementar mejoras
```

### Solo Restricciones Explícitas

```python
# Solo se detiene si una regla explícita lo requiere:
should_stop, rule = agent_rules.should_stop({
    'type': 'code_modification',
    'modified_files': ['kernel/src/f3/core.rs']  # Núcleo sagrado
})
# Returns: (True, rule) -> DETENER

should_stop, rule = agent_rules.should_stop({
    'type': 'code_modification',
    'modified_files': ['kernel/src/gui/mod.rs']  # No es núcleo sagrado
})
# Returns: (False, None) -> CONTINUAR CON LIBERTAD
```

## 📊 Verificación de Permisos

```python
# Verificar si una acción está permitida
is_allowed, blocking_rule = agent_rules.is_allowed("modify_file", {
    'file_path': 'kernel/src/gui/mod.rs',
    'type': 'code_modification'
})
# Returns: (True, None) -> PERMITIDO

is_allowed, blocking_rule = agent_rules.is_allowed("modify_file", {
    'file_path': 'kernel/src/f3/core.rs',
    'type': 'code_modification'
})
# Returns: (False, rule) -> PROHIBIDO (núcleo sagrado)
```

## 🎯 Resultado

El agente ahora:

1. ✅ **Tiene libertad total** para operar en F3-OS
2. ✅ **Solo respeta reglas explícitas** (núcleo sagrado, límites, coherencia)
3. ✅ **Opera únicamente en el proyecto** F3-OS
4. ✅ **Es proactivo y autónomo** sin restricciones innecesarias
5. ✅ **Puede implementar mejoras** libremente
6. ✅ **Puede aprender y aplicar** conocimiento sin límites

---

**El agente tiene total libertad para completar el propósito del proyecto F3-OS, respetando solo las reglas explícitas necesarias para proteger el núcleo sagrado y los recursos del sistema.**







