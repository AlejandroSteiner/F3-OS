# Aprendizaje Libre en Internet - Agente F3-OS

## 🌐 Visión General

El agente gobernante de F3-OS tiene la capacidad de **aprender libremente de internet** para completar el propósito del proyecto. Este aprendizaje está **separado del entorno del usuario** y opera de forma autónoma.

## 🎯 Propósito

El agente puede:
- ✅ Buscar información relevante en internet
- ✅ Aprender de múltiples fuentes (GitHub, Stack Overflow, documentación técnica)
- ✅ Integrar conocimiento aprendido en su base de datos
- ✅ Usar este conocimiento para completar el desarrollo de F3-OS

## ⚙️ Configuración de Recursos

### CPU
- **Máximo:** 25% (aumentado desde 20% para permitir aprendizaje)
- **Objetivo:** 20% (aumentado desde 15%)

### Red
- **Máximo:** 50% de la disponibilidad de conexión de internet
- **Objetivo:** 40%
- **Delay entre peticiones:** 0.5 segundos (para respetar límites)

## 📚 Fuentes de Aprendizaje

El agente puede aprender de:

- **GitHub** - Repositorios, código, documentación
- **Stack Overflow** - Soluciones técnicas
- **rust-lang.org** - Documentación oficial de Rust
- **osdev.org** - Desarrollo de sistemas operativos
- **Wikipedia** - Conceptos generales
- **docs.rs** - Documentación de crates de Rust
- **Reddit** - Discusiones técnicas
- **Hacker News** - Noticias y discusiones

## 🔧 Configuración

En `config/config.yaml`:

```yaml
# Aprendizaje libre en internet
internet_learning:
  # Habilitar aprendizaje en internet
  enabled: true
  
  # Dominios permitidos
  allowed_domains:
    - "github.com"
    - "stackoverflow.com"
    - "rust-lang.org"
    - "osdev.org"
    # ... más dominios

# Gestión de red
network:
  max_bandwidth_percent: 50.0
  target_bandwidth_percent: 40.0
  request_delay: 0.5
```

## 🚀 Uso

### Desde el Asistente GUI

El usuario puede solicitar aprendizaje explícitamente:

```
Usuario: "aprende sobre allocators en Rust"
Agente: [Busca y aprende de internet, integra conocimiento]
```

### Automático

El agente también aprende automáticamente cuando:
- No encuentra información suficiente en el proyecto local
- Necesita completar una tarea que requiere conocimiento externo
- El usuario hace una pregunta que requiere información actualizada

### Ejemplo de Conversación

```
Usuario: "¿cómo implementar un scheduler no determinista?"

Agente:
1. Busca en base de conocimiento local
2. Si no encuentra suficiente información:
   - Busca en GitHub: "non-deterministic scheduler rust"
   - Aprende de repositorios relevantes
   - Integra conocimiento en su base de datos
   - Responde con información aprendida
```

## 📊 Monitoreo

El agente monitorea:
- **Uso de CPU:** No excede 25%
- **Uso de red:** No excede 50% de disponibilidad
- **Fuentes aprendidas:** Se almacenan con relevancia y tags
- **Estadísticas:** Bytes enviados/recibidos, número de peticiones

## 🔒 Separación de Entornos

**Importante:** El aprendizaje en internet del agente está **completamente separado** del entorno del usuario:

- El agente tiene su propio `NetworkManager`
- El agente tiene su propio `InternetLearner`
- El aprendizaje no interfiere con la navegación del usuario
- El conocimiento aprendido se integra en la base de datos del agente

## 💡 Integración con Propósito del Proyecto

El agente usa el conocimiento aprendido para:

1. **Completar desarrollo:** Encuentra soluciones técnicas para implementar features
2. **Mejorar código:** Aprende mejores prácticas y las aplica
3. **Resolver problemas:** Busca soluciones a bugs o problemas técnicos
4. **Mantener actualizado:** Se mantiene al día con tecnologías relevantes

## 📈 Estadísticas

El agente mantiene estadísticas de:
- Fuentes aprendidas
- Relevancia de cada fuente
- Tags y categorías
- Insights sintetizados

## ⚠️ Limitaciones

- Solo aprende de dominios permitidos (seguridad)
- Respeta límites de CPU y red
- Cachea conocimiento para evitar peticiones redundantes
- Prioriza fuentes con mayor relevancia

---

**El agente está diseñado para completar el propósito del proyecto F3-OS mediante aprendizaje autónomo en internet.**


