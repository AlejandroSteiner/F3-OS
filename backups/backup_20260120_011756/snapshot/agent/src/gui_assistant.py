"""
GUI Assistant - Asistente/Amigo del usuario en la GUI de F3-OS

El agente gobernante también funciona como asistente amigable dentro de la GUI.
"""

import time
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


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
        
        # Respuestas predefinidas
        self._init_responses()
    
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
        
        # Saludos
        if any(word in input_lower for word in ['hola', 'hi', 'hello', 'saludo']):
            return 'greeting'
        
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
        
        # Ayuda general
        if any(word in input_lower for word in ['ayuda', 'help', 'qué puedes hacer']):
            return 'help'
        
        # Por defecto: conversación general
        return 'general'
    
    def _generate_response(self, intent: str, user_input: str, context: Optional[Dict]) -> str:
        """Genera respuesta según intención"""
        if intent == 'greeting':
            return f"¡Hola {self.state.user_name}! ¿En qué puedo ayudarte hoy?"
        
        elif intent == 'f3_model':
            response = self.help_responses.get('f3_model', '')
            if self.state.context_aware:
                response += f"\n\nActualmente el sistema está en fase {self.state.system_phase.upper()}."
            return response
        
        elif intent == 'phases':
            response = self.help_responses.get('phases', '')
            if context and 'current_phase' in context:
                response += f"\n\nFase actual: {context['current_phase'].upper()}"
            return response
        
        elif intent == 'navigation':
            return self.help_responses.get('navigation', 'Puedo ayudarte a navegar. ¿A dónde quieres ir?')
        
        elif intent == 'development':
            return self.help_responses.get('development', 'Soy el agente gobernante. ¿Tienes alguna pregunta sobre desarrollo?')
        
        elif intent == 'system_status':
            status = self.governance_core.get_status()
            response = f"📊 Estado del Sistema F3-OS:\n"
            response += f"- Fase: {status['phase'].upper()}\n"
            response += f"- Entropía: {status['entropy']}/255\n"
            response += f"- Perfection Score: {status['perfection_score']}\n"
            response += f"- Ciclos: {status['cycle_count']}\n"
            
            if 'resources' in status:
                cpu = status['resources'].get('cpu_percent', 0)
                response += f"- CPU del agente: {cpu:.1f}%\n"
            
            return response
        
        elif intent == 'help':
            response = "🤖 Puedo ayudarte con:\n"
            response += "- Explicar el modelo F3\n"
            response += "- Navegar por el sistema\n"
            response += "- Ver estado del sistema\n"
            response += "- Preguntas sobre desarrollo\n"
            response += "- Cualquier otra cosa relacionada con F3-OS\n\n"
            response += "¿Qué te gustaría saber?"
            return response
        
        else:  # general
            return self._generate_general_response(user_input)
    
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
            "¿Qué es el modelo F3?",
            "¿En qué fase está el sistema?",
            "Muéstrame el estado del sistema",
            "¿Cómo funciona el ciclo de fases?",
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

