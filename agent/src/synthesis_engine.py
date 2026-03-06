"""
Synthesis Engine - Equivalente a MEM Thread

Sintetiza propuestas y genera feedback.
"""

from typing import Dict, List, Optional


class SynthesisEngine:
    """Sintetiza métricas y genera feedback"""
    
    def __init__(self, config: dict):
        self.config = config
        self.use_ai = config.get('ai', {}).get('use_ai_synthesis', False)
        # TODO: Inicializar cliente AI si use_ai_synthesis es True
    
    def synthesize(self, code_metrics: Dict, context_info: Dict, phase_info: Dict) -> Dict:
        """
        Sintetiza métricas de diferentes fuentes
        
        Args:
            code_metrics: Métricas del Code Analyzer
            context_info: Información del Context Manager
            phase_info: Información de la fase actual
        
        Returns:
            Dict con síntesis y recomendaciones
        """
        synthesis = {
            'overall_score': 0,
            'recommendation': 'pending',
            'confidence': 0.0,
            'key_issues': [],
            'key_strengths': [],
            'feedback': '',
        }
        
        # Calcular score general
        synthesis['overall_score'] = self._calculate_overall_score(
            code_metrics, context_info, phase_info
        )
        
        # Identificar issues clave
        synthesis['key_issues'] = self._identify_issues(code_metrics, context_info)
        
        # Identificar fortalezas
        synthesis['key_strengths'] = self._identify_strengths(code_metrics, context_info)
        
        # Generar recomendación
        synthesis['recommendation'] = self._generate_recommendation(
            synthesis['overall_score'],
            synthesis['key_issues'],
            phase_info
        )
        
        # Calcular confianza
        synthesis['confidence'] = self._calculate_confidence(
            code_metrics, context_info, synthesis
        )
        
        # Generar feedback legible
        synthesis['feedback'] = self._generate_feedback(synthesis, code_metrics)
        
        return synthesis
    
    def _calculate_overall_score(self, code_metrics: Dict, context_info: Dict, phase_info: Dict) -> int:
        """Calcula score general (0-100)"""
        score = 50  # Base neutral
        
        # Score de coherencia F3 (peso alto)
        coherence = code_metrics.get('coherence_score', 50)
        score += (coherence - 50) * 0.4
        
        # Score de complejidad (invertido: menos complejo = mejor)
        complexity = code_metrics.get('complexity_score', 50)
        score += (100 - complexity - 50) * 0.2
        
        # Tamaño del PR
        if code_metrics.get('size_ok', True):
            score += 10
        else:
            score -= 20
        
        # Si toca núcleo sagrado sin discusión previa
        if code_metrics.get('touches_sacred_core', False):
            # En fase lógica o perfecta, penalizar más
            if phase_info.get('should_enforce_strictness', False):
                score -= 30
            else:
                score -= 15
        
        # Términos prohibidos
        forbidden_count = len(code_metrics.get('forbidden_terms_found', []))
        score -= forbidden_count * 15
        
        # Ajustar según fase
        if phase_info.get('should_allow_experimentation', False):
            # En fase ilógica, ser más permisivo
            score += 10
        
        return max(0, min(100, int(score)))
    
    def _identify_issues(self, code_metrics: Dict, context_info: Dict) -> List[str]:
        """Identifica issues clave"""
        issues = []
        
        if not code_metrics.get('size_ok', True):
            issues.append("PR demasiado grande (viola regla de PRs pequeños)")
        
        if code_metrics.get('touches_sacred_core', False):
            issues.append("Toca núcleo sagrado (requiere Issue [CONCEPTUAL] previo)")
        
        forbidden_terms = code_metrics.get('forbidden_terms_found', [])
        if forbidden_terms:
            issues.append(f"Usa términos prohibidos: {', '.join(forbidden_terms)}")
        
        if code_metrics.get('coherence_score', 100) < 70:
            issues.append("Baja coherencia con modelo F3")
        
        vocabulary_issues = code_metrics.get('vocabulary_issues', [])
        if vocabulary_issues:
            issues.append("Problemas con vocabulario F3")
        
        return issues
    
    def _identify_strengths(self, code_metrics: Dict, context_info: Dict) -> List[str]:
        """Identifica fortalezas"""
        strengths = []
        
        if code_metrics.get('size_ok', True) and code_metrics.get('total_lines', 0) < 100:
            strengths.append("PR pequeño y enfocado")
        
        if code_metrics.get('coherence_score', 0) >= 80:
            strengths.append("Alta coherencia con modelo F3")
        
        if not code_metrics.get('touches_sacred_core', False):
            strengths.append("No toca núcleo sagrado")
        
        if code_metrics.get('complexity_score', 100) < 50:
            strengths.append("Baja complejidad")
        
        if not code_metrics.get('forbidden_terms_found', []):
            strengths.append("Respeta vocabulario F3")
        
        return strengths
    
    def _generate_recommendation(self, score: int, issues: List[str], phase_info: Dict) -> str:
        """Genera recomendación basada en score y issues"""
        if score >= 80 and not issues:
            return 'approve'
        elif score >= 60 and len(issues) <= 1:
            # En fase ilógica, ser más permisivo
            if phase_info.get('should_allow_experimentation', False):
                return 'approve'
            return 'approve_with_caution'
        elif score >= 40:
            return 'request_changes'
        else:
            return 'reject'
    
    def _calculate_confidence(self, code_metrics: Dict, context_info: Dict, synthesis: Dict) -> float:
        """Calcula confianza en la síntesis (0.0-1.0)"""
        confidence = 0.5  # Base
        
        # Más información = más confianza
        if code_metrics.get('total_lines', 0) > 0:
            confidence += 0.2
        
        # Decisiones similares en el pasado = más confianza
        similar_decisions = context_info.get('similar_decisions', [])
        if similar_decisions:
            confidence += 0.2
        
        # Menos issues = más confianza
        issues_count = len(synthesis.get('key_issues', []))
        confidence -= issues_count * 0.1
        
        # Score extremo (muy alto o muy bajo) = más confianza
        score = synthesis.get('overall_score', 50)
        if score >= 80 or score <= 30:
            confidence += 0.1
        
        return max(0.0, min(1.0, confidence))
    
    def _generate_feedback(self, synthesis: Dict, code_metrics: Dict) -> str:
        """Genera feedback legible para humanos"""
        feedback = []
        
        feedback.append("## 🤖 Evaluación del Agente F3-OS\n")
        feedback.append(f"**Score General**: {synthesis['overall_score']}/100")
        feedback.append(f"**Confianza**: {synthesis['confidence']:.0%}")
        feedback.append(f"**Recomendación**: {synthesis['recommendation']}\n")
        
        if synthesis['key_strengths']:
            feedback.append("### ✅ Fortalezas")
            for strength in synthesis['key_strengths']:
                feedback.append(f"- {strength}")
            feedback.append("")
        
        if synthesis['key_issues']:
            feedback.append("### ⚠️ Issues")
            for issue in synthesis['key_issues']:
                feedback.append(f"- {issue}")
            feedback.append("")
        
        # Métricas detalladas
        feedback.append("### 📊 Métricas Detalladas")
        feedback.append(f"- Líneas: {code_metrics.get('total_lines', 0)}")
        feedback.append(f"- Archivos: {code_metrics.get('files_affected', 0)}")
        feedback.append(f"- Coherencia F3: {code_metrics.get('coherence_score', 0)}/100")
        feedback.append(f"- Complejidad: {code_metrics.get('complexity_score', 0)}/100")
        
        # Recomendación específica
        feedback.append("\n### 💡 Recomendación")
        recommendation = synthesis['recommendation']
        if recommendation == 'approve':
            feedback.append("✅ Este PR está alineado con el modelo F3 y puede ser aprobado.")
        elif recommendation == 'approve_with_caution':
            feedback.append("⚠️ Este PR puede ser aprobado, pero revisa los issues mencionados.")
        elif recommendation == 'request_changes':
            feedback.append("🔄 Este PR necesita cambios antes de ser aprobado.")
        elif recommendation == 'reject':
            feedback.append("❌ Este PR no está alineado con el modelo F3 y debe ser rechazado.")
        
        return '\n'.join(feedback)







