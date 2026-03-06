# Capacidades del Asistente GUI

El asistente GUI de F3-OS ahora tiene capacidad autónoma para analizar el proyecto y responder preguntas específicas basándose en el contenido real de los archivos del proyecto.

## 🧠 Nuevas Capacidades

### 1. Análisis de Archivos del Proyecto

El asistente puede leer y analizar automáticamente los siguientes archivos:

- `MANIFIESTO.md` - Filosofía y principios del proyecto
- `REGLAS_LOGICA.md` - Reglas y ciclo de fases
- `CONTRIBUTING.md` - Reglas de contribución
- `GOVERNANCE.md` - Gobernanza y núcleo sagrado
- `README.md` - Información general
- `ARQUITECTURA_COMPLETA.md` - Arquitectura técnica
- `SEGURIDAD_Y_RESISTENCIA.md` - Análisis de seguridad
- `AGENTE_GOBERNANTE.md` - Documentación del agente

### 2. Preguntas que Puede Responder

#### 📋 Reglas del Proyecto
**Ejemplos:**
- "¿Cuáles son tus reglas?"
- "¿Cuáles son las reglas del proyecto?"
- "Explícame todas tus reglas"

**Respuesta:** El asistente analiza y presenta:
- Principios fundamentales del manifiesto
- Reglas de lógica F3-OS
- Reglas de contribución
- Reglas de gobernanza (núcleo sagrado)

#### 📚 Explicación desde Cero
**Ejemplos:**
- "Explicame desde cero"
- "Analiza los archivos del proyecto"
- "Comprender el proyecto"

**Respuesta:** El asistente proporciona:
- ¿Qué es F3-OS?
- ¿Qué NO es F3-OS?
- El Modelo F3 completo
- Principios fundamentales

#### 🔷 Modelo F3
**Ejemplos:**
- "¿Qué es el modelo F3?"
- "Explícame el modelo"
- "¿Cómo funcionan los hilos?"

**Respuesta:** Explicación detallada del modelo F3 basada en los archivos del proyecto.

#### 🔄 Ciclo de Fases
**Ejemplos:**
- "¿Cómo funciona el ciclo de fases?"
- "Explícame las fases"
- "¿Qué es la fase ilógica?"

**Respuesta:** Explicación completa del ciclo de 4 fases (Lógico → Ilógico → Síntesis → Perfecto).

#### 💻 Desarrollo
**Ejemplos:**
- "¿Cómo contribuir?"
- "¿Cuáles son las reglas de desarrollo?"
- "Preguntas sobre desarrollo"

**Respuesta:** Reglas fundamentales de contribución y desarrollo.

#### 🔍 Búsqueda Inteligente
**Ejemplos:**
- Cualquier pregunta sobre el proyecto

**Respuesta:** El asistente busca en todos los archivos del proyecto y proporciona información relevante encontrada.

### 3. Respuestas Conversacionales + Acciones Ejecutables

El asistente **responde Y ejecuta** para las siguientes instrucciones:

#### 👋 Saludos y Estado
- **"Hola, ¿cómo estás?"** → Responde amigablemente
- **"¿Qué estás haciendo?"** / **"¿En qué trabajas ahora?"** → Muestra actividad reciente real del agente
- **"¿Estás conectado a internet?"** → Verifica la conexión y responde con el resultado real

#### 📥 Descargar
- **"Busca este enlace y descarga esta aplicación: https://..."** → Descarga el archivo y lo guarda en `agent/downloads/`
- Incluye una URL en tu mensaje para que descargue

#### 📦 Instalar
- **"Instala requests"** / **"Instala el paquete numpy"** → Ejecuta `pip install` del paquete indicado

#### 🔧 Trabajar sobre Aplicación
- **"Trabaja sobre kernel"** / **"Trabaja sobre agent/gui_assistant.py"** → Analiza el archivo o directorio y sugiere siguientes pasos

## 🎯 Cómo Funciona

### ProjectAnalyzer

El módulo `project_analyzer.py` proporciona:

1. **Lectura de archivos con cache**: Los archivos se leen una vez y se cachean para respuestas rápidas.

2. **Extracción de secciones**: Analiza documentos Markdown y extrae secciones por encabezados.

3. **Búsqueda inteligente**: Busca texto en múltiples archivos y proporciona contexto.

4. **Métodos especializados**:
   - `get_rules()` - Obtiene todas las reglas del proyecto
   - `get_f3_model_explanation()` - Explicación completa del modelo F3
   - `explain_from_scratch()` - Explicación completa desde cero
   - `get_section()` - Obtiene una sección específica
   - `search_in_files()` - Busca texto en archivos

### Detección de Intenciones Mejorada

El asistente ahora detecta:

- **Saludos**: "hola", "cómo estás", "qué tal"
- **Actividad actual**: "qué estás haciendo", "en qué trabajas"
- **Internet**: "estás conectado", "tienes internet"
- **Descargar**: "descarga", "descargar", "busca este enlace"
- **Instalar**: "instala", "instalar paquete"
- **Trabajar sobre**: "trabaja sobre", "trabaja en", "analiza esta aplicación"
- **Reglas**: "reglas", "rules", "tus reglas"
- **Explicación desde cero**: "explicame desde cero", "analiza"
- **Modelo F3**: "f3", "modelo", "hilos", "embudo"
- **Fases**: "fase", "lógico", "ilógico", "síntesis", "perfecto"
- **Desarrollo**: "desarrollo", "pr", "código", "contribuir"
- **Estado**: "estado", "status", "fase actual"
- **Ayuda**: "ayuda", "help", "qué puedes hacer"

## 🚀 Uso

### Iniciar el Servidor GUI

```bash
cd agent
./run.sh gui-server
```

### Acceder a la Interfaz

Abre tu navegador en: `http://localhost:8080`

### Ejemplos de Conversación

```
Usuario: Hola
Asistente: ¡Hola Usuario! ¿En qué puedo ayudarte hoy?

Usuario: ¿Cuáles son tus reglas?
Asistente: 📋 Reglas del Proyecto F3-OS:
[Presenta todas las reglas del proyecto]

Usuario: Explicame desde cero
Asistente: 📚 Explicación Completa de F3-OS desde Cero:
[Explicación completa basada en los archivos]

Usuario: ¿Qué es el modelo F3?
Asistente: 🔷 Modelo F3:
[Explicación detallada del modelo F3]
```

## 📝 Notas Técnicas

- El analizador encuentra automáticamente la raíz del proyecto (subiendo desde `agent/`)
- Los archivos se cachean en memoria para respuestas rápidas
- Si un archivo no se encuentra, el asistente proporciona una respuesta alternativa
- Las respuestas se formatean con Markdown para mejor legibilidad
- El asistente mantiene contexto de la conversación

## 🔧 Configuración

El `project_root` se calcula automáticamente, pero puede configurarse en `config/config.yaml`:

```yaml
project_root: "/ruta/al/proyecto/f3-os"
```

## ✅ Mejoras Futuras

- [ ] Búsqueda semántica más avanzada
- [ ] Respuestas más contextuales basadas en historial
- [ ] Soporte para más tipos de archivos
- [ ] Análisis de código fuente (Rust)
- [ ] Generación de diagramas explicativos







