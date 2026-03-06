"""
GUI Assistant - Asistente/Amigo del usuario en la GUI de F3-OS

El agente gobernante también funciona como asistente amigable dentro de la GUI.
"""

import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging

from .project_analyzer import ProjectAnalyzer
from .project_knowledge_base import ProjectKnowledgeBase
from .action_executor import ActionExecutor

logger = logging.getLogger(__name__)


class AssistantPersonality(Enum):
    """Personalidad del asistente"""
    FRIENDLY = "friendly"      # Amigable y conversacional
    TECHNICAL = "technical"    # Técnico y preciso
    ADAPTIVE = "adaptive"      # Se adapta al contexto


@dataclass
class Message:
    """Mensaje en la conversación"""
    role: str  # "user" o "assistant"
    content: str
    timestamp: datetime
    context: Optional[Dict] = None


@dataclass
class AssistantState:
    """Estado del asistente"""
    personality: AssistantPersonality
    conversation_history: List[Message]
    user_name: str
    system_phase: str  # Fase actual del sistema F3
    context_aware: bool


class GUIAssistant:
    """Asistente GUI del agente gobernante"""
    
    def __init__(self, config: dict, governance_core, resource_manager):
        self.config = config
        self.governance_core = governance_core
        self.resource_manager = resource_manager
        
        # Personalidad del asistente
        personality_str = config.get('gui_assistant', {}).get('personality', 'adaptive')
        self.personality = AssistantPersonality[personality_str.upper()]
        
        # Estado del asistente
        self.state = AssistantState(
            personality=self.personality,
            conversation_history=[],
            user_name=config.get('gui_assistant', {}).get('user_name', 'Usuario'),
            system_phase='logical',
            context_aware=True
        )
        
        # Base de conocimiento completa (regla primaria)
        project_root = config.get('project_root', None)
        self.knowledge_base = ProjectKnowledgeBase(project_root=project_root)
        
        # Analizador de proyecto (para búsquedas específicas)
        self.project_analyzer = ProjectAnalyzer(project_root=project_root)
        
        # Aprendizaje en internet (separado del entorno del usuario)
        if hasattr(governance_core, 'internet_learner'):
            self.internet_learner = governance_core.internet_learner
        else:
            from .internet_learning import InternetLearner, NetworkManager
            network_manager = NetworkManager(config)
            self.internet_learner = InternetLearner(config, network_manager)
        
        # Ejecutor de acciones (descargar, instalar, trabajar sobre apps)
        project_root = config.get('project_root', Path(__file__).parent.parent.parent)
        self.action_executor = ActionExecutor(config, project_root)
        
        # Respuestas predefinidas
        self._init_responses()
        
        logger.info("GUIAssistant inicializado con base de conocimiento completa y aprendizaje en internet")
    
    def _init_responses(self):
        """Inicializa respuestas y patrones de conversación"""
        self.greetings = [
            "¡Hola! Soy tu asistente F3-OS. ¿En qué puedo ayudarte?",
            "Hola, soy el agente gobernante de F3-OS. ¿Qué necesitas?",
            "¡Bienvenido! Estoy aquí para ayudarte con F3-OS.",
        ]
        
        self.help_responses = {
            'f3_model': "F3-OS usa un modelo de 3 hilos (CPU, RAM, MEM) que convergen en un embudo central. El sistema opera en un ciclo: Lógico → Ilógico → Síntesis → Perfecto.",
            'phases': "El sistema tiene 4 fases: LÓGICO (ordenado), ILÓGICO (exploración), SÍNTESIS (concentración), PERFECTO (optimizado). Cada ciclo mejora el sistema.",
            'navigation': "Puedo ayudarte a navegar por el sistema. ¿Qué quieres hacer?",
            'development': "Como agente gobernante, evalúo PRs y mantengo coherencia con el modelo F3. ¿Tienes alguna pregunta sobre desarrollo?",
        }
    
    def greet(self) -> str:
        """Saludo inicial del asistente"""
        greeting = self.greetings[0]  # Puede ser aleatorio
        message = Message(
            role="assistant",
            content=greeting,
            timestamp=datetime.now()
        )
        self.state.conversation_history.append(message)
        return greeting
    
    def process_message(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Procesa mensaje del usuario y genera respuesta"""
        # Aplicar throttling de recursos
        if self.resource_manager:
            from .resource_manager import ThrottledOperation
            with ThrottledOperation(self.resource_manager):
                return self._process_message_internal(user_input, context)
        else:
            return self._process_message_internal(user_input, context)
    
    def _process_message_internal(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Procesa mensaje internamente"""
        # Registrar actividad de procesamiento
        from .activity_stream import log_thinking
        log_thinking(f"Procesando consulta del usuario: {user_input[:50]}...")
        
        # Guardar mensaje del usuario
        user_message = Message(
            role="user",
            content=user_input,
            timestamp=datetime.now(),
            context=context
        )
        self.state.conversation_history.append(user_message)
        
        # Actualizar contexto del sistema
        if context:
            self.state.system_phase = context.get('system_phase', self.state.system_phase)
        
        # Analizar intención
        intent = self._analyze_intent(user_input)
        
        # Generar respuesta según intención
        response = self._generate_response(intent, user_input, context)
        
        # Guardar respuesta
        assistant_message = Message(
            role="assistant",
            content=response,
            timestamp=datetime.now(),
            context={'intent': intent}
        )
        self.state.conversation_history.append(assistant_message)
        
        return response
    
    def _analyze_intent(self, user_input: str) -> str:
        """Analiza la intención del usuario"""
        input_lower = user_input.lower()
        
        # Saludos (incluye "hola como estas")
        if any(word in input_lower for word in ['hola', 'hi', 'hello', 'saludo', 'buenos días', 'buenas tardes']):
            return 'greeting'
        
        # Preguntas sobre reglas (alta prioridad)
        if any(word in input_lower for word in ['reglas', 'rules', 'tus reglas', 'las reglas', 'reglas del proyecto']):
            return 'rules'
        
        # Explicar desde cero / analizar archivos
        if any(phrase in input_lower for phrase in ['explicame desde cero', 'explica desde cero', 'desde cero', 
                                                     'analiza', 'analizar', 'lee los archivos', 'lee archivos',
                                                     'comprender el proyecto', 'entender el proyecto']):
            return 'explain_from_scratch'
        
        # Preguntas sobre F3
        if any(word in input_lower for word in ['f3', 'modelo', 'hilos', 'embudo']):
            return 'f3_model'
        
        # Preguntas sobre fases
        if any(word in input_lower for word in ['fase', 'phase', 'lógico', 'ilógico', 'síntesis', 'perfecto']):
            return 'phases'
        
        # Navegación
        if any(word in input_lower for word in ['navegar', 'ir', 'abrir', 'mostrar', 'ver']):
            return 'navigation'
        
        # Desarrollo
        if any(word in input_lower for word in ['desarrollo', 'pr', 'código', 'contribuir']):
            return 'development'
        
        # Estado del sistema
        if any(word in input_lower for word in ['estado', 'status', 'fase actual', 'qué está pasando']):
            return 'system_status'
        
        # ¿Qué estás haciendo? / ¿En qué trabajas?
        if any(phrase in input_lower for phrase in ['qué estás haciendo', 'que estas haciendo', 'en qué trabajas',
                                                     'en que trabajas', 'qué haces ahora', 'que haces ahora',
                                                     'qué haces', 'que haces', 'en qué trabajas ahora']):
            return 'current_activity'
        
        # ¿Estás conectado a internet?
        if any(phrase in input_lower for phrase in ['estás conectado', 'estas conectado', 'tienes internet',
                                                     'hay internet', 'conexión a internet', 'conexion a internet',
                                                     'conectado a internet']):
            return 'internet_status'
        
        # Busca y descarga / descarga desde enlace
        if any(word in input_lower for word in ['descarga', 'descargar', 'descargame', 'descárgame',
                                                 'busca este enlace', 'busca el enlace', 'descarga esta aplicación',
                                                 'descarga esta app']) or ('enlace' in input_lower and 'descargar' in input_lower):
            return 'download_action'
        
        # Instala aplicación
        if any(phrase in input_lower for phrase in ['instala', 'instalar', 'instala esta aplicación',
                                                     'instala esta app', 'instala el paquete', 'instala la aplicación']):
            return 'install_action'
        
        # Trabaja sobre esta aplicación
        if any(phrase in input_lower for phrase in ['trabaja sobre', 'trabaja en', 'trabaja con',
                                                     'trabaja en esta aplicación', 'trabaja sobre esta aplicación',
                                                     'trabaja sobre esta app', 'analiza esta aplicación']):
            return 'work_on_app'
        
        # Ayuda general
        if any(word in input_lower for word in ['ayuda', 'help', 'qué puedes hacer']):
            return 'help'
        
        # Preguntas que requieren aprendizaje en internet
        if any(word in input_lower for word in ['aprender', 'internet', 'buscar', 'investigar', 'cómo hacer', 'tutorial']):
            return 'internet_learning'
        
        # Por defecto: conversación general
        return 'general'
    
    def _generate_response(self, intent: str, user_input: str, context: Optional[Dict]) -> str:
        """Genera respuesta según intención"""
        if intent == 'greeting':
            # Incluye "hola como estas", "hola que tal"
            input_lower = user_input.lower()
            if any(p in input_lower for p in ['cómo estás', 'como estas', 'qué tal', 'que tal', 'how are you']):
                return (f"¡Hola {self.state.user_name}! Estoy bien, gracias. "
                        "Listo para ayudarte con F3-OS. ¿En qué puedo colaborar hoy?")
            return f"¡Hola {self.state.user_name}! ¿En qué puedo ayudarte hoy?"
        
        elif intent == 'rules':
            # Obtener TODAS las reglas desde la base de conocimiento completa
            logger.info("Usuario pregunta sobre reglas - usando base de conocimiento completa...")
            
            # Primero intentar obtener reglas de .cursorrules (prioridad)
            cursorrules_content = self.knowledge_base.get_project_rules_content()
            if cursorrules_content and "F3-OS Project Rules" in cursorrules_content:
                response = "📋 **REGLAS DEL PROYECTO F3-OS (.cursorrules):**\n\n"
                response += "Estas son las reglas principales que el agente debe seguir:\n\n"
                response += "---\n\n"
                
                # Mostrar resumen estructurado
                rules_summary = self.knowledge_base.get_complete_rules()
                if rules_summary:
                    response += rules_summary
                else:
                    # Si no hay resumen, mostrar contenido completo (limitado)
                    lines = cursorrules_content.split('\n')
                    response += '\n'.join(lines[:200])  # Primeras 200 líneas
                    if len(lines) > 200:
                        response += f"\n\n... (Total: {len(lines)} líneas. ¿Quieres que profundice en alguna sección específica?)"
                
                response += "\n\n💡 **Nota**: Estas reglas definen cómo el agente debe comportarse al trabajar en F3-OS."
            else:
                # Fallback a reglas extraídas
                rules = self.knowledge_base.get_complete_rules()
                if rules:
                    rules_lines = rules.split('\n')
                    if len(rules_lines) > 150:
                        response = "📋 **Todas las Reglas del Proyecto F3-OS:**\n\n"
                        response += '\n'.join(rules_lines[:150])
                        response += f"\n\n... (Total: {len(rules_lines)} reglas. ¿Quieres que profundice en alguna específica?)"
                    else:
                        response = "📋 **Todas las Reglas del Proyecto F3-OS:**\n\n" + rules
                else:
                    # Fallback al analizador
                    rules = self.project_analyzer.get_rules()
                    response = "📋 **Reglas del Proyecto F3-OS:**\n\n" + (rules if rules else "No se encontraron reglas documentadas.")
            
            return response
        
        elif intent == 'explain_from_scratch':
            # Explicación completa desde cero usando base de conocimiento
            logger.info("Usuario pide explicación desde cero - usando base de conocimiento completa...")
            overview = self.knowledge_base.get_project_overview()
            human_functions = self.knowledge_base.get_human_functions()
            
            response = "📚 **Explicación Completa de F3-OS desde Cero (Base de Conocimiento Completa):**\n\n"
            response += overview
            response += "\n\n" + human_functions
            response += "\n\n¿Hay algo específico que quieras que profundice?"
            return response
        
        elif intent == 'f3_model':
            # Usar analizador para obtener explicación detallada
            f3_explanation = self.project_analyzer.get_f3_model_explanation()
            if f3_explanation:
                response = "🔷 **Modelo F3:**\n\n" + f3_explanation
            else:
                response = self.help_responses.get('f3_model', '')
            
            if self.state.context_aware:
                response += f"\n\nActualmente el sistema está en fase {self.state.system_phase.upper()}."
            return response
        
        elif intent == 'phases':
            # Obtener explicación detallada de fases
            phases_section = self.project_analyzer.get_section('reglas', 'el ciclo de 4 fases')
            if phases_section:
                response = "🔄 **Ciclo de 4 Fases:**\n\n" + phases_section
            else:
                response = self.help_responses.get('phases', '')
            
            if context and 'current_phase' in context:
                response += f"\n\n**Fase actual:** {context['current_phase'].upper()}"
            return response
        
        elif intent == 'navigation':
            return self.help_responses.get('navigation', 'Puedo ayudarte a navegar. ¿A dónde quieres ir?')
        
        elif intent == 'development':
            # Obtener información sobre desarrollo
            contributing_section = self.project_analyzer.get_section('contributing', 'reglas fundamentales')
            if contributing_section:
                response = "💻 **Desarrollo en F3-OS:**\n\n"
                response += contributing_section
                response += "\n\nComo agente gobernante, evalúo PRs y mantengo coherencia con el modelo F3."
            else:
                response = self.help_responses.get('development', 'Soy el agente gobernante. ¿Tienes alguna pregunta sobre desarrollo?')
            return response
        
        elif intent == 'current_activity':
            # Respuesta + ejecuta: obtiene actividad real
            activity = self.action_executor.get_current_activity()
            return f"📋 **En qué trabajo ahora:**\n\n{activity}"
        
        elif intent == 'internet_status':
            # Respuesta + ejecuta: verifica conexión real
            connected, message = self.action_executor.check_internet_connection()
            return f"🌐 **Conexión a Internet:**\n\n{message}"
        
        elif intent == 'download_action':
            # Ejecuta: extrae URL y descarga
            url = self.action_executor.extract_url_from_text(user_input)
            if not url:
                return ("⚠️ No encontré ninguna URL en tu mensaje.\n\n"
                        "Por favor, incluye el enlace. Ejemplo: "
                        "\"Descarga esta aplicación: https://ejemplo.com/app.zip\"")
            
            result = self.action_executor.download_from_url(url)
            if result['success']:
                return (f"✅ **Descarga completada:**\n\n"
                        f"Archivo guardado en: `{result['path']}`\n"
                        f"Tamaño: {result['size']:,} bytes\n"
                        f"Nombre: {result['filename']}")
            else:
                return f"❌ **Error al descargar:**\n\n{result['error']}"
        
        elif intent == 'install_action':
            # Ejecuta: extrae nombre del paquete y instala
            # Buscar nombres de paquete (palabras tras "instala")
            input_lower = user_input.lower()
            package = None
            for prefix in ['instala', 'instalar']:
                if prefix in input_lower:
                    rest = user_input.split(prefix, 1)[-1].strip()
                    # Quitar puntuación y tomar primera palabra o conjunto
                    words = re.findall(r'[\w\-\.]+', rest)
                    if words:
                        package = words[0]  # Primer token
                    break
            
            if not package or len(package) < 2:
                return ("⚠️ No pude identificar qué paquete instalar.\n\n"
                        "Por favor especifica: \"Instala requests\" o \"Instala el paquete numpy\"")
            
            result = self.action_executor.install_package(package)
            if result['success']:
                return f"✅ **Paquete instalado:**\n\n{package} instalado correctamente."
            else:
                return f"❌ **Error al instalar {package}:**\n\n{result.get('error', result.get('output', 'Error desconocido'))}"
        
        elif intent == 'work_on_app':
            # Ejecuta: extrae ruta/nombre y analiza
            input_lower = user_input.lower()
            path = None
            for prefix in ['trabaja sobre', 'trabaja en', 'trabaja con', 'analiza esta', 'trabaja en esta', 'trabaja sobre esta']:
                if prefix in input_lower:
                    rest = user_input.split(prefix, 1)[-1].strip()
                    rest = rest.replace('aplicación', '').replace('aplicacion', '').replace('app', '').strip(' :,.-')
                    if rest:
                        path = rest
                    break
            
            if not path:
                # Usar proyecto actual
                path = '.'
            
            result = self.action_executor.work_on_application(path)
            if result['success']:
                response = f"📂 **Análisis de {path}:**\n\n{result['analysis']}\n\n"
                if result.get('suggestions'):
                    response += "**Siguientes pasos posibles:**\n"
                    for s in result['suggestions']:
                        response += f"- {s}\n"
                return response
            else:
                return f"❌ **No pude trabajar sobre eso:**\n\n{result.get('error', 'Error desconocido')}"
        
        elif intent == 'system_status':
            status = self.governance_core.get_status()
            response = f"📊 **Estado del Sistema F3-OS:**\n\n"
            response += f"- **Fase:** {status['phase'].upper()}\n"
            response += f"- **Entropía:** {status['entropy']}/255\n"
            response += f"- **Perfection Score:** {status['perfection_score']}\n"
            response += f"- **Ciclos:** {status['cycle_count']}\n"
            
            if 'resources' in status:
                cpu = status['resources'].get('cpu_percent', 0)
                response += f"- **CPU del agente:** {cpu:.1f}%\n"
            
            return response
        
        elif intent == 'help':
            response = "🤖 **Puedo ayudarte con:**\n\n"
            response += "- 👋 Saludar y conversar (\"hola, ¿cómo estás?\")\n"
            response += "- 📋 Explicar las reglas del proyecto\n"
            response += "- 🔷 Explicar el modelo F3\n"
            response += "- 🔄 Explicar el ciclo de fases\n"
            response += "- 📊 Ver estado del sistema\n"
            response += "- 📍 Saber en qué trabajo (\"¿qué estás haciendo?\")\n"
            response += "- 🌐 Verificar conexión a internet\n"
            response += "- 📥 **Descargar** archivos (incluye URL en tu mensaje)\n"
            response += "- 📦 **Instalar** paquetes pip (\"instala requests\")\n"
            response += "- 🔧 **Trabajar sobre** apps o archivos del proyecto\n"
            response += "- 🌐 Aprender de internet\n\n"
            response += "¿Qué te gustaría hacer?"
            return response
        
        elif intent == 'internet_learning':
            # Aprendizaje libre en internet (separado del entorno del usuario)
            logger.info(f"Aprendizaje en internet solicitado: {user_input}")
            
            # Registrar actividad de pensamiento
            from .activity_stream import log_thinking
            log_thinking(f"Analizando solicitud de aprendizaje: {user_input}")
            
            # Extraer query de aprendizaje
            learning_query = user_input
            if 'aprender' in learning_query.lower():
                learning_query = learning_query.replace('aprender', '').replace('sobre', '').strip()
            
            # Buscar y aprender de internet
            learned_sources = self.internet_learner.search_and_learn(learning_query, max_results=3)
            
            if learned_sources:
                response = f"🌐 **Aprendiendo de Internet (50% de red disponible):**\n\n"
                response += f"He encontrado {len(learned_sources)} fuentes relevantes:\n\n"
                
                for i, source in enumerate(learned_sources, 1):
                    response += f"**{i}. {source.title}**\n"
                    response += f"   URL: {source.url}\n"
                    response += f"   Relevancia: {source.relevance_score:.2f}\n"
                    response += f"   Tags: {', '.join(source.tags[:3])}\n"
                    response += f"   Contenido: {source.content[:200]}...\n\n"
                
                # Aplicar conocimiento aprendido
                applied = self.internet_learner.apply_learned_knowledge({'query': learning_query})
                if applied.get('insights'):
                    response += "**Insights:**\n"
                    for insight in applied['insights']:
                        response += f"- {insight}\n"
                
                response += "\n💡 Este conocimiento se ha integrado en mi base de datos para completar el propósito del proyecto."
            else:
                response = f"⚠️ No pude encontrar fuentes relevantes para '{learning_query}'.\n"
                response += "¿Podrías reformular tu pregunta o ser más específico?"
            
            return response
        
        else:  # general
            # Resolución inmediata usando base de conocimiento completa
            logger.info(f"Resolviendo consulta inmediata: {user_input[:50]}...")
            immediate_response = self.knowledge_base.resolve_query_immediate(user_input)
            
            if immediate_response and "no encontrada" not in immediate_response.lower():
                response = f"🔍 **Respuesta Inmediata (Base de Conocimiento Completa):**\n\n"
                response += immediate_response
                response += "\n\n¿Necesitas más información sobre algún aspecto específico?"
            else:
                # Fallback: búsqueda en archivos
                search_results = self.project_analyzer.search_in_files(user_input)
                if search_results:
                    response = f"🔍 **Encontré información relacionada con tu pregunta:**\n\n"
                    for filename, content in search_results[:3]:
                        response += f"**En {filename}:**\n{content[:500]}...\n\n"
                    response += "¿Quieres que profundice en algún aspecto específico?"
                else:
                    # Si no hay información local, intentar aprender de internet
                    logger.info(f"No se encontró información local, intentando aprendizaje en internet: {user_input}")
                    learned_sources = self.internet_learner.search_and_learn(user_input, max_results=2)
                    
                    if learned_sources:
                        response = f"🌐 **No encontré información local, pero aprendí de internet:**\n\n"
                        for source in learned_sources:
                            response += f"**{source.title}**\n"
                            response += f"{source.content[:300]}...\n"
                            response += f"Fuente: {source.url}\n\n"
                        response += "💡 Este conocimiento se ha integrado para completar el propósito del proyecto."
                    else:
                        return self._generate_general_response(user_input)
            return response
    
    def _generate_general_response(self, user_input: str) -> str:
        """Genera respuesta general conversacional"""
        # Respuestas amigables según personalidad
        if self.state.personality == AssistantPersonality.FRIENDLY:
            responses = [
                "Interesante pregunta. Déjame pensar...",
                "Eso es algo que puedo ayudarte a entender.",
                "Buena pregunta. Te explico:",
            ]
            return f"{responses[0]} ¿Podrías ser más específico sobre qué te interesa de F3-OS?"
        
        elif self.state.personality == AssistantPersonality.TECHNICAL:
            return "Necesito más contexto técnico. ¿Podrías especificar qué aspecto de F3-OS te interesa?"
        
        else:  # ADAPTIVE
            # Adaptarse según historial
            if len(self.state.conversation_history) > 2:
                return "Basándome en nuestra conversación, creo que te interesa el modelo F3. ¿Quieres que te explique algo específico?"
            else:
                return "¿Podrías ser más específico? Puedo ayudarte con el modelo F3, navegación, o desarrollo."
    
    def get_conversation_history(self, limit: Optional[int] = None) -> List[Message]:
        """Obtiene historial de conversación"""
        if limit:
            return self.state.conversation_history[-limit:]
        return self.state.conversation_history
    
    def clear_history(self) -> None:
        """Limpia historial de conversación"""
        self.state.conversation_history = []
    
    def update_system_context(self, context: Dict) -> None:
        """Actualiza contexto del sistema"""
        if 'system_phase' in context:
            self.state.system_phase = context['system_phase']
    
    def get_suggestions(self) -> List[str]:
        """Obtiene sugerencias de preguntas/comandos"""
        suggestions = [
            "¿Hola, cómo estás?",
            "¿Qué estás haciendo ahora?",
            "¿Estás conectado a internet?",
            "¿Cuáles son tus reglas?",
            "Explicame desde cero",
            "¿Qué es el modelo F3?",
            "¿En qué fase está el sistema?",
            "¿Qué puedes hacer?",
        ]
        return suggestions
    
    def get_personality(self) -> str:
        """Obtiene personalidad actual"""
        return self.state.personality.value


class GUIWindow:
    """Representa una ventana de GUI para el asistente"""
    
    def __init__(self, assistant: GUIAssistant):
        self.assistant = assistant
        self.is_open = False
        self.position = {'x': 100, 'y': 100}
        self.size = {'width': 600, 'height': 400}
    
    def open(self) -> None:
        """Abre la ventana del asistente"""
        self.is_open = True
        greeting = self.assistant.greet()
        return greeting
    
    def close(self) -> None:
        """Cierra la ventana"""
        self.is_open = False
    
    def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        """Envía mensaje al asistente"""
        if not self.is_open:
            self.open()
        return self.assistant.process_message(message, context)
    
    def render(self) -> Dict:
        """Renderiza la ventana (para integración con GUI real)"""
        return {
            'is_open': self.is_open,
            'position': self.position,
            'size': self.size,
            'conversation': [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat()
                }
                for msg in self.assistant.get_conversation_history(limit=20)
            ],
            'suggestions': self.assistant.get_suggestions(),
        }

