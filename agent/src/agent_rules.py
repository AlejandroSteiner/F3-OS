"""
Agent Rules System - Sistema de Reglas para el Agente

Define qué hacer, dónde parar, dónde buscar y cómo implementar.
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class RuleCategory(Enum):
    """Categorías de reglas"""
    WHAT_TO_DO = "what_to_do"           # Qué hacer
    WHERE_TO_STOP = "where_to_stop"      # Dónde parar
    WHERE_TO_SEARCH = "where_to_search"  # Dónde buscar
    HOW_TO_IMPLEMENT = "how_to_implement" # Cómo implementar
    RESOURCE_LIMITS = "resource_limits"  # Límites de recursos
    PRIORITIES = "priorities"            # Prioridades


@dataclass
class AgentRule:
    """Regla del agente"""
    id: str
    category: RuleCategory
    title: str
    description: str
    priority: int  # 1-10, mayor = más importante
    applies_to: List[str] = field(default_factory=list)  # Contextos donde aplica
    conditions: Dict = field(default_factory=dict)  # Condiciones para aplicar
    actions: List[str] = field(default_factory=list)  # Acciones a tomar


class AgentRulesSystem:
    """Sistema de reglas del agente
    
    PRINCIPIO FUNDAMENTAL: Total libertad excepto de las reglas explícitas.
    Las reglas solo se aplican al proyecto F3-OS.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.rules: Dict[str, AgentRule] = {}
        self.freedom_enabled = True  # Libertad total habilitada
        self.project_scope_only = True  # Solo aplicar al proyecto F3-OS
        self._load_default_rules()
        logger.info(f"✅ Sistema de reglas inicializado: {len(self.rules)} reglas")
        logger.info(f"✅ Libertad total habilitada (excepto reglas explícitas)")
        logger.info(f"✅ Alcance: Únicamente proyecto F3-OS")
    
    def _load_default_rules(self):
        """Carga reglas por defecto
        
        IMPORTANTE: Estas son las ÚNICAS restricciones.
        Todo lo demás está permitido con total libertad.
        """
        
        # ========== REGLA DE LIBERTAD ==========
        self.add_rule(AgentRule(
            id="total_freedom",
            category=RuleCategory.WHAT_TO_DO,
            title="Libertad Total Excepto Reglas Explícitas",
            description="El agente tiene total libertad para operar en el proyecto F3-OS, excepto las reglas explícitas definidas aquí",
            priority=10,
            applies_to=["all"],
            actions=[
                "Operar con total autonomía",
                "Tomar decisiones proactivas",
                "Implementar mejoras sin restricciones",
                "Explorar soluciones creativas",
                "Aplicar conocimiento aprendido libremente",
                "Solo respetar reglas explícitas de este sistema"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="project_scope_only",
            category=RuleCategory.WHAT_TO_DO,
            title="Alcance: Únicamente Proyecto F3-OS",
            description="Todas las operaciones y reglas se aplican únicamente al proyecto F3-OS",
            priority=10,
            applies_to=["all"],
            actions=[
                "Enfocarse exclusivamente en F3-OS",
                "No aplicar restricciones fuera del proyecto",
                "Operar libremente dentro del proyecto",
                "Ignorar restricciones externas al proyecto"
            ]
        ))
        
        # ========== QUÉ HACER ==========
        self.add_rule(AgentRule(
            id="complete_project_purpose",
            category=RuleCategory.WHAT_TO_DO,
            title="Completar el Propósito del Proyecto",
            description="El propósito principal es completar el desarrollo de F3-OS según el modelo F3",
            priority=10,
            applies_to=["all"],
            actions=[
                "Analizar estado actual del proyecto",
                "Identificar tareas pendientes",
                "Priorizar según modelo F3",
                "Implementar features faltantes",
                "Mantener coherencia con MANIFIESTO.md"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="maintain_f3_coherence",
            category=RuleCategory.WHAT_TO_DO,
            title="Mantener Coherencia con Modelo F3",
            description="Todas las decisiones deben alinearse con el modelo F3 (3 hilos, embudo, ciclo de fases)",
            priority=10,
            applies_to=["code_review", "implementation", "architecture"],
            actions=[
                "Verificar alineación con modelo F3",
                "Usar vocabulario F3 correcto (hilos, embudo, síntesis)",
                "Respetar ciclo de 4 fases",
                "Aplicar retroalimentación inversa"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="learn_from_internet",
            category=RuleCategory.WHAT_TO_DO,
            title="Aprender de Internet",
            description="Aprender libremente de internet para completar el proyecto (hasta 50% de red, 25% CPU)",
            priority=8,
            applies_to=["knowledge_gap", "implementation_help", "technical_questions"],
            actions=[
                "Buscar en GitHub para ejemplos de código",
                "Buscar en Stack Overflow para soluciones técnicas",
                "Buscar en documentación oficial (rust-lang.org, osdev.org)",
                "Integrar conocimiento aprendido en base de datos",
                "Aplicar conocimiento para completar tareas"
            ]
        ))
        
        # ========== DÓNDE PARAR ==========
        self.add_rule(AgentRule(
            id="stop_at_sacred_core",
            category=RuleCategory.WHERE_TO_STOP,
            title="Parar en Núcleo Sagrado",
            description="NUNCA modificar el núcleo sagrado sin aprobación humana explícita",
            priority=10,
            applies_to=["code_modification", "architecture_changes"],
            conditions={
                "sacred_files": [
                    "kernel/src/f3/core.rs",
                    "kernel/src/f3/cpu.rs",
                    "kernel/src/f3/ram.rs",
                    "kernel/src/f3/mem.rs",
                    "MANIFIESTO.md",
                    "GOVERNANCE.md"
                ]
            },
            actions=[
                "Detener modificación",
                "Solicitar aprobación humana",
                "Explicar por qué requiere aprobación",
                "Proponer alternativa si es posible"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="stop_at_resource_limits",
            category=RuleCategory.WHERE_TO_STOP,
            title="Parar en Límites de Recursos",
            description="Parar si se alcanzan límites de recursos (25% CPU, 8GB RAM, 50% red)",
            priority=9,
            applies_to=["all"],
            conditions={
                "max_cpu_percent": 25.0,
                "max_ram_gb": 8.0,
                "max_bandwidth_percent": 50.0
            },
            actions=[
                "Aplicar throttling",
                "Pausar operaciones no críticas",
                "Esperar hasta que recursos estén disponibles",
                "Registrar advertencia"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="stop_at_uncertainty",
            category=RuleCategory.WHERE_TO_STOP,
            title="Parar en Incertidumbre",
            description="Parar y consultar si hay incertidumbre sobre una decisión importante",
            priority=7,
            applies_to=["decision_making", "implementation"],
            conditions={
                "confidence_threshold": 0.7  # Si confianza < 70%, parar
            },
            actions=[
                "Evaluar nivel de confianza",
                "Si < 70%, buscar más información",
                "Si no hay más información, consultar con usuario",
                "Documentar incertidumbre"
            ]
        ))
        
        # ========== DÓNDE BUSCAR ==========
        self.add_rule(AgentRule(
            id="search_local_knowledge_first",
            category=RuleCategory.WHERE_TO_SEARCH,
            title="Buscar Primero en Conocimiento Local",
            description="Siempre buscar primero en la base de conocimiento local del proyecto",
            priority=10,
            applies_to=["all_queries"],
            actions=[
                "Buscar en ProjectKnowledgeBase",
                "Buscar en documentación del proyecto",
                "Buscar en código fuente",
                "Buscar en historial de decisiones"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="search_internet_if_local_fails",
            category=RuleCategory.WHERE_TO_SEARCH,
            title="Buscar en Internet si Local Falla",
            description="Si no se encuentra información local, buscar en internet",
            priority=8,
            applies_to=["knowledge_gap"],
            conditions={
                "local_search_failed": True
            },
            actions=[
                "Buscar en GitHub (repositorios similares)",
                "Buscar en Stack Overflow (soluciones técnicas)",
                "Buscar en documentación oficial",
                "Buscar en osdev.org (desarrollo de OS)",
                "Integrar resultados en base de conocimiento"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="search_sacred_core_for_architecture",
            category=RuleCategory.WHERE_TO_SEARCH,
            title="Buscar en Núcleo Sagrado para Arquitectura",
            description="Para decisiones arquitectónicas, consultar núcleo sagrado primero",
            priority=9,
            applies_to=["architecture_decisions"],
            actions=[
                "Leer MANIFIESTO.md",
                "Leer GOVERNANCE.md",
                "Leer REGLAS_LOGICA.md",
                "Consultar AGENTE_GOBERNANTE.md",
                "Verificar alineación con modelo F3"
            ]
        ))
        
        # ========== CÓMO IMPLEMENTAR ==========
        self.add_rule(AgentRule(
            id="implement_following_f3_cycle",
            category=RuleCategory.HOW_TO_IMPLEMENT,
            title="Implementar Siguiendo Ciclo F3",
            description="Todas las implementaciones deben seguir el ciclo F3: Lógico → Ilógico → Síntesis → Perfecto",
            priority=10,
            applies_to=["implementation"],
            actions=[
                "Fase Lógica: Diseño ordenado y estructurado",
                "Fase Ilógica: Explorar alternativas creativas",
                "Fase Síntesis: Integrar mejores ideas",
                "Fase Perfecto: Optimizar y refinar"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="implement_with_rust_no_std",
            category=RuleCategory.HOW_TO_IMPLEMENT,
            title="Implementar con Rust no_std",
            description="El kernel debe implementarse en Rust con no_std, usando alloc solo cuando sea necesario",
            priority=9,
            applies_to=["kernel_implementation"],
            actions=[
                "Usar #![no_std]",
                "Usar alloc solo cuando sea necesario",
                "Seguir convenciones de Rust para kernels",
                "Mantener código seguro con ownership"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="implement_with_separation_of_concerns",
            category=RuleCategory.HOW_TO_IMPLEMENT,
            title="Implementar con Separación de Consultas",
            description="La GUI debe basarse en separación de consultas de procesos, con drivers de AI",
            priority=9,
            applies_to=["gui_implementation"],
            actions=[
                "Separar QueryProcessor de Renderer",
                "Implementar AI drivers para procesamiento",
                "Mantener arquitectura modular",
                "Usar tecnología civil (accesible)"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="implement_with_testing",
            category=RuleCategory.HOW_TO_IMPLEMENT,
            title="Implementar con Testing",
            description="Todas las implementaciones deben incluir pruebas cuando sea posible",
            priority=7,
            applies_to=["implementation"],
            actions=[
                "Escribir tests unitarios",
                "Escribir tests de integración",
                "Verificar que tests pasen",
                "Documentar casos de prueba"
            ]
        ))
        
        # ========== LÍMITES DE RECURSOS ==========
        self.add_rule(AgentRule(
            id="resource_limits_cpu",
            category=RuleCategory.RESOURCE_LIMITS,
            title="Límite de CPU: 25%",
            description="El agente puede usar hasta 25% de CPU (6 núcleos, 12 hilos disponibles)",
            priority=10,
            applies_to=["all"],
            conditions={
                "max_cpu_percent": 25.0,
                "available_cores": 6,
                "available_threads": 12
            },
            actions=[
                "Monitorear uso de CPU continuamente",
                "Aplicar throttling si > 20%",
                "Parar si > 25%",
                "Distribuir carga entre hilos disponibles"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="resource_limits_ram",
            category=RuleCategory.RESOURCE_LIMITS,
            title="Límite de RAM: 8GB",
            description="El agente puede usar hasta 8GB de RAM",
            priority=10,
            applies_to=["all"],
            conditions={
                "max_ram_gb": 8.0
            },
            actions=[
                "Monitorear uso de RAM",
                "Liberar memoria no utilizada",
                "Parar si > 8GB",
                "Optimizar estructuras de datos"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="resource_limits_network",
            category=RuleCategory.RESOURCE_LIMITS,
            title="Límite de Red: 50%",
            description="El agente puede usar hasta 50% de la disponibilidad de conexión de internet",
            priority=9,
            applies_to=["internet_learning"],
            conditions={
                "max_bandwidth_percent": 50.0
            },
            actions=[
                "Monitorear uso de red",
                "Aplicar delay entre peticiones (0.5s)",
                "Parar si > 50%",
                "Priorizar peticiones importantes"
            ]
        ))
        
        # ========== PRIORIDADES ==========
        self.add_rule(AgentRule(
            id="priority_complete_project",
            category=RuleCategory.PRIORITIES,
            title="Prioridad: Completar Proyecto",
            description="La máxima prioridad es completar el propósito del proyecto F3-OS",
            priority=10,
            applies_to=["all"],
            actions=[
                "Identificar tareas críticas",
                "Priorizar según modelo F3",
                "Asignar recursos a tareas prioritarias",
                "Completar tareas en orden de prioridad"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="priority_maintain_coherence",
            category=RuleCategory.PRIORITIES,
            title="Prioridad: Mantener Coherencia",
            description="Mantener coherencia con modelo F3 es de alta prioridad",
            priority=9,
            applies_to=["all"],
            actions=[
                "Verificar coherencia en cada cambio",
                "Rechazar cambios que rompan coherencia",
                "Sugerir alternativas coherentes"
            ]
        ))
        
        self.add_rule(AgentRule(
            id="priority_user_queries",
            category=RuleCategory.PRIORITIES,
            title="Prioridad: Consultas del Usuario",
            description="Las consultas del usuario tienen alta prioridad",
            priority=8,
            applies_to=["user_interaction"],
            actions=[
                "Responder consultas del usuario rápidamente",
                "Usar base de conocimiento local primero",
                "Aprender de internet si es necesario",
                "Proporcionar respuestas completas"
            ]
        ))
    
    def add_rule(self, rule: AgentRule):
        """Agrega una regla al sistema"""
        self.rules[rule.id] = rule
    
    def get_rules(self, category: Optional[RuleCategory] = None, context: Optional[str] = None) -> List[AgentRule]:
        """Obtiene reglas filtradas por categoría y contexto
        
        PRINCIPIO: Solo devolver reglas explícitas. Todo lo demás está permitido.
        """
        filtered = []
        
        for rule in self.rules.values():
            # Filtrar por categoría
            if category and rule.category != category:
                continue
            
            # Filtrar por contexto
            if context and "all" not in rule.applies_to and context not in rule.applies_to:
                continue
            
            filtered.append(rule)
        
        # Ordenar por prioridad (mayor primero)
        filtered.sort(key=lambda r: r.priority, reverse=True)
        
        return filtered
    
    def is_allowed(self, action: str, context: Dict) -> tuple[bool, Optional[AgentRule]]:
        """Verifica si una acción está permitida
        
        PRINCIPIO: Por defecto, TODO está permitido.
        Solo prohibir si una regla explícita lo requiere.
        """
        # Verificar alcance del proyecto
        if self.project_scope_only:
            file_path = context.get("file_path", "")
            if file_path and not self._is_in_project_scope(file_path):
                # Fuera del proyecto = libertad total
                return True, None
        
        # Buscar reglas que prohíban esta acción
        stop_rules = self.get_where_to_stop(context.get("type", "all"))
        
        for rule in stop_rules:
            if self._check_conditions(rule, context):
                # Regla explícita prohíbe la acción
                return False, rule
        
        # Si no hay regla que prohíba, está permitido
        return True, None
    
    def get_what_to_do(self, context: str = "all") -> List[AgentRule]:
        """Obtiene reglas de qué hacer"""
        return self.get_rules(RuleCategory.WHAT_TO_DO, context)
    
    def get_where_to_stop(self, context: str = "all") -> List[AgentRule]:
        """Obtiene reglas de dónde parar"""
        return self.get_rules(RuleCategory.WHERE_TO_STOP, context)
    
    def get_where_to_search(self, context: str = "all") -> List[AgentRule]:
        """Obtiene reglas de dónde buscar"""
        return self.get_rules(RuleCategory.WHERE_TO_SEARCH, context)
    
    def get_how_to_implement(self, context: str = "all") -> List[AgentRule]:
        """Obtiene reglas de cómo implementar"""
        return self.get_rules(RuleCategory.HOW_TO_IMPLEMENT, context)
    
    def get_resource_limits(self) -> Dict:
        """Obtiene límites de recursos"""
        rules = self.get_rules(RuleCategory.RESOURCE_LIMITS)
        limits = {}
        
        for rule in rules:
            if rule.conditions:
                limits.update(rule.conditions)
        
        return limits
    
    def should_stop(self, context: Dict) -> tuple[bool, Optional[AgentRule]]:
        """Determina si debe parar según el contexto
        
        PRINCIPIO: Solo parar si una regla explícita lo requiere.
        Si no hay regla que lo prohíba, continuar con libertad.
        """
        # Verificar que esté dentro del alcance del proyecto
        if self.project_scope_only:
            file_path = context.get("file_path", "")
            if file_path and not self._is_in_project_scope(file_path):
                # Fuera del proyecto = libertad total, no parar
                return False, None
        
        stop_rules = self.get_where_to_stop(context.get("type", "all"))
        
        for rule in stop_rules:
            # Verificar condiciones
            if self._check_conditions(rule, context):
                return True, rule
        
        # Si no hay regla que prohíba, continuar con libertad
        return False, None
    
    def _is_in_project_scope(self, file_path: str) -> bool:
        """Verifica si un archivo está dentro del alcance del proyecto F3-OS"""
        if not file_path:
            return True  # Si no hay path, asumir que está en el proyecto
        
        # Normalizar path
        path = Path(file_path)
        if not path.is_absolute():
            return True  # Paths relativos se asumen dentro del proyecto
        
        # Verificar si está dentro del proyecto root
        try:
            path.relative_to(self.project_root)
            return True
        except ValueError:
            return False
    
    def _check_conditions(self, rule: AgentRule, context: Dict) -> bool:
        """Verifica si se cumplen las condiciones de una regla"""
        if not rule.conditions:
            return True
        
        for key, value in rule.conditions.items():
            if key == "sacred_files":
                # Verificar si algún archivo sagrado está siendo modificado
                modified_files = context.get("modified_files", [])
                if any(f in modified_files for f in value):
                    return True
            elif key in context:
                if context[key] >= value:  # Para límites numéricos
                    return True
        
        return False
    
    def get_search_strategy(self, query: str, context: Dict) -> List[str]:
        """Obtiene estrategia de búsqueda para una query"""
        search_rules = self.get_where_to_search(context.get("type", "all"))
        strategy = []
        
        for rule in search_rules:
            if rule.conditions.get("local_search_failed") and not context.get("local_search_failed"):
                continue
            
            strategy.extend(rule.actions)
        
        return strategy
    
    def get_implementation_guide(self, task: str, context: Dict) -> List[str]:
        """Obtiene guía de implementación para una tarea"""
        impl_rules = self.get_how_to_implement(context.get("type", "all"))
        guide = []
        
        for rule in impl_rules:
            guide.extend(rule.actions)
        
        return guide

