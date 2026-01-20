"""
GUI Integration - Integración del asistente con la GUI de F3-OS

Proporciona interfaz para que el asistente funcione dentro de la GUI del sistema.
"""

from typing import Dict, Optional, Callable
from .gui_assistant import GUIAssistant, GUIWindow
from .governance_core import GovernanceCore
from .resource_manager import ResourceManager


class GUIIntegration:
    """Integración del asistente con la GUI de F3-OS"""
    
    def __init__(self, governance_core: GovernanceCore, resource_manager: ResourceManager, config: dict):
        self.governance_core = governance_core
        self.resource_manager = resource_manager
        self.config = config
        
        # Crear asistente
        self.assistant = GUIAssistant(config, governance_core, resource_manager)
        
        # Ventana del asistente
        self.window = GUIWindow(self.assistant)
        
        # Callbacks para integración con GUI real
        self.render_callback: Optional[Callable] = None
        self.update_callback: Optional[Callable] = None
    
    def open_assistant(self) -> str:
        """Abre la ventana del asistente"""
        greeting = self.window.open()
        
        # Actualizar contexto del sistema
        status = self.governance_core.get_status()
        self.assistant.update_system_context({
            'system_phase': status['phase'],
            'entropy': status['entropy'],
            'perfection_score': status['perfection_score'],
        })
        
        # Notificar a GUI si hay callback
        if self.update_callback:
            self.update_callback(self.window.render())
        
        return greeting
    
    def close_assistant(self) -> None:
        """Cierra la ventana del asistente"""
        self.window.close()
        if self.update_callback:
            self.update_callback(self.window.render())
    
    def send_message(self, message: str) -> str:
        """Envía mensaje al asistente"""
        # Obtener contexto actual del sistema
        status = self.governance_core.get_status()
        context = {
            'system_phase': status['phase'],
            'entropy': status['entropy'],
            'perfection_score': status['perfection_score'],
            'current_phase': status['phase'],
        }
        
        # Procesar mensaje
        response = self.window.send_message(message, context)
        
        # Notificar a GUI si hay callback
        if self.update_callback:
            self.update_callback(self.window.render())
        
        return response
    
    def get_suggestions(self) -> list:
        """Obtiene sugerencias de preguntas"""
        return self.assistant.get_suggestions()
    
    def get_conversation(self, limit: Optional[int] = None) -> list:
        """Obtiene historial de conversación"""
        return [
            {
                'role': msg.role,
                'content': msg.content,
                'timestamp': msg.timestamp.isoformat()
            }
            for msg in self.assistant.get_conversation_history(limit=limit)
        ]
    
    def register_render_callback(self, callback: Callable) -> None:
        """Registra callback para renderizado de GUI"""
        self.render_callback = callback
    
    def register_update_callback(self, callback: Callable) -> None:
        """Registra callback para actualizaciones de GUI"""
        self.update_callback = callback
    
    def get_window_state(self) -> Dict:
        """Obtiene estado de la ventana para renderizado"""
        return self.window.render()
    
    def toggle_assistant(self) -> Optional[str]:
        """Alterna estado del asistente (abrir/cerrar)"""
        if self.window.is_open:
            self.close_assistant()
            return None
        else:
            return self.open_assistant()
    
    def update_system_context(self) -> None:
        """Actualiza contexto del sistema en el asistente"""
        status = self.governance_core.get_status()
        self.assistant.update_system_context({
            'system_phase': status['phase'],
            'entropy': status['entropy'],
            'perfection_score': status['perfection_score'],
        })


# API simplificada para integración con GUI del kernel
class AssistantAPI:
    """API simplificada para usar desde el kernel/GUI"""
    
    def __init__(self, gui_integration: GUIIntegration):
        self.gui = gui_integration
    
    def open(self) -> str:
        """Abre asistente"""
        return self.gui.open_assistant()
    
    def close(self) -> None:
        """Cierra asistente"""
        self.gui.close_assistant()
    
    def ask(self, question: str) -> str:
        """Hace pregunta al asistente"""
        return self.gui.send_message(question)
    
    def is_open(self) -> bool:
        """Verifica si está abierto"""
        return self.gui.window.is_open
    
    def get_state(self) -> Dict:
        """Obtiene estado para renderizado"""
        return self.gui.get_window_state()

