"""
Activity Stream - Flujo de Actividades del Agente

Muestra en tiempo real lo que el agente está haciendo:
- Consultas en internet
- Cambios en código
- Ejecución de comandos
- Compilación
- etc.
"""

import logging
import threading
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import json

logger = logging.getLogger(__name__)


class ActivityType(Enum):
    """Tipos de actividades"""
    INTERNET_SEARCH = "internet_search"
    INTERNET_LEARN = "internet_learn"
    FILE_CREATE = "file_create"
    FILE_MODIFY = "file_modify"
    FILE_DELETE = "file_delete"
    COMMAND_EXECUTE = "command_execute"
    BUILD = "build"
    TEST = "test"
    CODE_ANALYSIS = "code_analysis"
    DECISION = "decision"
    LEARNING = "learning"
    THINKING = "thinking"
    ERROR = "error"
    SUCCESS = "success"


@dataclass
class Activity:
    """Actividad del agente"""
    id: str
    type: ActivityType
    title: str
    description: str
    timestamp: datetime
    status: str = "running"  # running, success, error, warning
    details: Dict = None
    duration_ms: Optional[int] = None
    
    def to_dict(self):
        """Convierte a diccionario para JSON"""
        data = asdict(self)
        data['type'] = self.type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data


class ActivityStream:
    """Flujo de actividades del agente en tiempo real"""
    
    def __init__(self, max_activities: int = 1000):
        self.max_activities = max_activities
        self.activities: List[Activity] = []
        self.subscribers: List[callable] = []
        self.lock = threading.Lock()
        self.activity_counter = 0
        
        logger.info("✅ Activity Stream inicializado")
    
    def subscribe(self, callback: callable):
        """Suscribe un callback para recibir actividades en tiempo real"""
        with self.lock:
            self.subscribers.append(callback)
    
    def unsubscribe(self, callback: callable):
        """Desuscribe un callback"""
        with self.lock:
            if callback in self.subscribers:
                self.subscribers.remove(callback)
    
    def _notify_subscribers(self, activity: Activity):
        """Notifica a todos los suscriptores"""
        with self.lock:
            for callback in self.subscribers:
                try:
                    callback(activity)
                except Exception as e:
                    logger.error(f"Error notificando actividad: {e}")
    
    def add_activity(self, activity_type: ActivityType, title: str, description: str = "", 
                    status: str = "running", details: Dict = None) -> Activity:
        """Agrega una nueva actividad"""
        self.activity_counter += 1
        activity = Activity(
            id=f"activity_{self.activity_counter}",
            type=activity_type,
            title=title,
            description=description,
            timestamp=datetime.now(),
            status=status,
            details=details or {}
        )
        
        with self.lock:
            self.activities.append(activity)
            # Mantener solo las últimas N actividades
            if len(self.activities) > self.max_activities:
                self.activities = self.activities[-self.max_activities:]
        
        # Notificar suscriptores
        self._notify_subscribers(activity)
        
        logger.info(f"📊 Actividad: {activity_type.value} - {title}")
        
        return activity
    
    def update_activity(self, activity_id: str, status: str = None, 
                       description: str = None, details: Dict = None, duration_ms: int = None):
        """Actualiza una actividad existente"""
        with self.lock:
            for activity in self.activities:
                if activity.id == activity_id:
                    if status:
                        activity.status = status
                    if description:
                        activity.description = description
                    if details:
                        activity.details.update(details)
                    if duration_ms:
                        activity.duration_ms = duration_ms
                    
                    # Notificar actualización
                    self._notify_subscribers(activity)
                    break
    
    def get_recent_activities(self, limit: int = 50) -> List[Dict]:
        """Obtiene actividades recientes"""
        with self.lock:
            recent = self.activities[-limit:]
            return [a.to_dict() for a in recent]
    
    def get_activities_by_type(self, activity_type: ActivityType, limit: int = 50) -> List[Dict]:
        """Obtiene actividades por tipo"""
        with self.lock:
            filtered = [a for a in self.activities if a.type == activity_type]
            recent = filtered[-limit:]
            return [a.to_dict() for a in recent]
    
    def clear(self):
        """Limpia todas las actividades"""
        with self.lock:
            self.activities.clear()
            self.activity_counter = 0


# Instancia global del stream
_global_stream: Optional[ActivityStream] = None


def get_activity_stream() -> ActivityStream:
    """Obtiene la instancia global del stream"""
    global _global_stream
    if _global_stream is None:
        _global_stream = ActivityStream()
    return _global_stream


def log_internet_search(query: str, results_count: int = 0):
    """Registra búsqueda en internet"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.INTERNET_SEARCH,
        f"🔍 Buscando en internet: {query}",
        f"Encontradas {results_count} fuentes",
        details={'query': query, 'results_count': results_count}
    )


def log_internet_learn(url: str, title: str = ""):
    """Registra aprendizaje de internet"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.INTERNET_LEARN,
        f"🌐 Aprendiendo de: {title or url}",
        f"URL: {url}",
        details={'url': url, 'title': title}
    )


def log_file_create(file_path: str):
    """Registra creación de archivo"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.FILE_CREATE,
        f"📄 Creando archivo: {file_path}",
        f"Ruta: {file_path}",
        details={'file_path': file_path}
    )


def log_file_modify(file_path: str, changes_count: int = 0):
    """Registra modificación de archivo"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.FILE_MODIFY,
        f"✏️  Modificando: {file_path}",
        f"{changes_count} cambios aplicados",
        details={'file_path': file_path, 'changes_count': changes_count}
    )


def log_command_execute(command: str):
    """Registra ejecución de comando"""
    stream = get_activity_stream()
    activity = stream.add_activity(
        ActivityType.COMMAND_EXECUTE,
        f"⚙️  Ejecutando: {command}",
        "Comando en progreso...",
        details={'command': command}
    )
    return activity


def log_build():
    """Registra compilación del proyecto"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.BUILD,
        "🔨 Compilando proyecto F3-OS",
        "Ejecutando build.sh...",
        details={}
    )


def log_test():
    """Registra ejecución de tests"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.TEST,
        "🧪 Ejecutando tests",
        "Verificando que todo funciona...",
        details={}
    )


def log_decision(decision: str, reason: str = ""):
    """Registra una decisión del agente"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.DECISION,
        f"🎯 Decisión: {decision}",
        reason,
        status="success",
        details={'decision': decision, 'reason': reason}
    )


def log_thinking(thought: str):
    """Registra pensamiento del agente"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.THINKING,
        f"💭 Pensando: {thought}",
        "",
        details={'thought': thought}
    )


def log_error(error: str, details: Dict = None):
    """Registra un error"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.ERROR,
        f"❌ Error: {error}",
        "",
        status="error",
        details=details or {}
    )


def log_success(message: str):
    """Registra un éxito"""
    stream = get_activity_stream()
    return stream.add_activity(
        ActivityType.SUCCESS,
        f"✅ {message}",
        "",
        status="success",
        details={}
    )


