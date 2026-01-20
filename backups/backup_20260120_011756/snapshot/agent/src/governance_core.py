"""
Governance Core - Equivalente a F3 Core

Toma decisiones finales basadas en síntesis de todos los componentes.
"""

from typing import Dict, Optional
from .code_analyzer import CodeAnalyzer
from .context_manager import ContextManager
from .synthesis_engine import SynthesisEngine
from .development_phase import DevelopmentCycle
from .resource_manager import ResourceManager, ThrottledOperation


class GovernanceCore:
    """Núcleo de gobierno que toma decisiones finales"""
    
    def __init__(self, config: dict, data_dir):
        self.config = config
        self.code_analyzer = CodeAnalyzer(config)
        self.context_manager = ContextManager(config, data_dir)
        self.synthesis_engine = SynthesisEngine(config)
        self.development_cycle = DevelopmentCycle(config)
        self.resource_manager = ResourceManager(config)
        # Iniciar monitoreo de recursos
        self.resource_manager.start_monitoring()
    
    def evaluate_pr(self, pr_data: Dict) -> Dict:
        """
        Evalúa un PR completo y toma decisión
        
        Args:
            pr_data: Datos del PR desde GitHub API
        
        Returns:
            Dict con decisión y justificación
        """
        # Usar throttling para mantener uso de CPU bajo
        with ThrottledOperation(self.resource_manager):
            # 1. Analizar código (Code Analyzer)
            files_changed = pr_data.get('files', [])
            diff_content = pr_data.get('diff', '')
            code_metrics = self.code_analyzer.analyze_pr(files_changed, diff_content)
        
            # 2. Obtener contexto (Context Manager)
            similar_decisions = self.context_manager.get_similar_decisions(code_metrics)
            context_info = {
                'similar_decisions': similar_decisions,
                'project_context': self.context_manager.context,
            }
            
            # 3. Obtener información de fase (Development Cycle)
            phase_state = self.development_cycle.get_state()
            phase_info = {
                'current_phase': phase_state.phase.value,
                'should_allow_experimentation': self.development_cycle.should_allow_experimentation(),
                'should_enforce_strictness': self.development_cycle.should_enforce_strictness(),
                'entropy': phase_state.entropy,
                'perfection_score': phase_state.perfection_score,
            }
            
            # 4. Sintetizar (Synthesis Engine)
            synthesis = self.synthesis_engine.synthesize(
                code_metrics, context_info, phase_info
            )
            
            # 5. Tomar decisión final (Governance Core)
            decision = self._make_decision(
                synthesis, code_metrics, pr_data, phase_info
            )
            
            # 6. Registrar decisión
            self.context_manager.record_decision(
                pr_data.get('number', 0),
                decision['action'],
                decision['reason'],
                code_metrics
            )
            
            # 7. Actualizar ciclo de desarrollo
            self.development_cycle.process_pr({
                'approved': decision['action'] == 'approve',
                'experimental': phase_info['should_allow_experimentation'],
            })
        
        return {
            'decision': decision,
            'synthesis': synthesis,
            'code_metrics': code_metrics,
            'phase_info': phase_info,
            'feedback': synthesis['feedback'],
        }
    
    def _make_decision(self, synthesis: Dict, code_metrics: Dict, pr_data: Dict, phase_info: Dict) -> Dict:
        """Toma decisión final basada en síntesis"""
        recommendation = synthesis['recommendation']
        score = synthesis['overall_score']
        issues = synthesis['key_issues']
        
        # Verificar límites duros (nunca se violan)
        if self._violates_hard_limits(code_metrics, pr_data):
            return {
                'action': 'reject',
                'reason': 'Violación de límites duros del modelo F3',
                'auto': False,  # Requiere revisión humana
            }
        
        # Auto-aprobar si cumple criterios y está en fase apropiada
        auto_approve = self.config.get('evaluation', {}).get('auto_approve_small', False)
        auto_threshold = self.config.get('evaluation', {}).get('auto_approve_threshold', 50)
        
        if (auto_approve and 
            code_metrics.get('total_lines', 0) < auto_threshold and
            score >= 80 and
            not issues and
            not code_metrics.get('touches_sacred_core', False)):
            return {
                'action': 'approve',
                'reason': 'PR pequeño, bien alineado con modelo F3',
                'auto': True,
            }
        
        # Decisión basada en recomendación
        if recommendation == 'approve':
            return {
                'action': 'approve',
                'reason': synthesis['feedback'],
                'auto': False,
            }
        elif recommendation == 'approve_with_caution':
            return {
                'action': 'approve',
                'reason': f"Aprobado con precaución. {synthesis['feedback']}",
                'auto': False,
            }
        elif recommendation == 'request_changes':
            return {
                'action': 'request_changes',
                'reason': synthesis['feedback'],
                'auto': False,
            }
        else:  # reject
            return {
                'action': 'reject',
                'reason': synthesis['feedback'],
                'auto': False,
            }
    
    def _violates_hard_limits(self, code_metrics: Dict, pr_data: Dict) -> bool:
        """Verifica si se violan límites duros"""
        # Límite 1: PRs que tocan núcleo sagrado sin Issue [CONCEPTUAL]
        if code_metrics.get('touches_sacred_core', False):
            # Verificar si hay Issue [CONCEPTUAL] relacionado
            # TODO: Verificar en GitHub si hay Issue relacionado
            # Por ahora, asumimos que requiere revisión humana
            pass
        
        # Límite 2: PRs extremadamente grandes
        max_size = self.config.get('evaluation', {}).get('max_pr_size', 300)
        if code_metrics.get('total_lines', 0) > max_size * 2:
            return True
        
        # Límite 3: Múltiples términos prohibidos
        if len(code_metrics.get('forbidden_terms_found', [])) > 3:
            return True
        
        return False
    
    def get_status(self) -> Dict:
        """Obtiene estado actual del agente"""
        cycle_state = self.development_cycle.get_state()
        context_summary = self.context_manager.get_context_summary()
        resource_stats = self.resource_manager.get_resource_stats()
        
        return {
            'phase': cycle_state.phase.value,
            'entropy': cycle_state.entropy,
            'perfection_score': cycle_state.perfection_score,
            'cycle_count': cycle_state.cycle_count,
            'context': context_summary,
            'resources': resource_stats,
        }

