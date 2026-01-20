"""
Code Analyzer - Equivalente a CPU Thread

Analiza código propuesto y reporta métricas.
"""

import re
from typing import Dict, List, Tuple
from pathlib import Path


class CodeAnalyzer:
    """Analiza código según criterios F3"""
    
    def __init__(self, config: dict):
        self.config = config
        self.sacred_core = set(config.get('f3_model', {}).get('sacred_core', []))
        self.vocabulary = set(config.get('f3_model', {}).get('vocabulary', []))
        self.forbidden_terms = set(config.get('f3_model', {}).get('forbidden_terms', []))
        self.max_pr_size = config.get('evaluation', {}).get('max_pr_size', 300)
    
    def analyze_pr(self, files_changed: List[Dict], diff_content: str) -> Dict:
        """
        Analiza un PR y retorna métricas
        
        Args:
            files_changed: Lista de archivos modificados con sus cambios
            diff_content: Contenido del diff completo
        
        Returns:
            Dict con métricas de análisis
        """
        metrics = {
            'total_lines': self._count_lines(diff_content),
            'files_affected': len(files_changed),
            'touches_sacred_core': False,
            'vocabulary_issues': [],
            'forbidden_terms_found': [],
            'size_ok': True,
            'complexity_score': 0,
            'coherence_score': 0,
        }
        
        # Verificar si toca núcleo sagrado
        for file_info in files_changed:
            file_path = file_info.get('filename', '')
            if self._is_sacred_core(file_path):
                metrics['touches_sacred_core'] = True
                break
        
        # Verificar tamaño
        if metrics['total_lines'] > self.max_pr_size:
            metrics['size_ok'] = False
        
        # Analizar vocabulario y términos prohibidos
        vocabulary_issues, forbidden_terms = self._analyze_vocabulary(diff_content)
        metrics['vocabulary_issues'] = vocabulary_issues
        metrics['forbidden_terms_found'] = forbidden_terms
        
        # Calcular scores
        metrics['complexity_score'] = self._calculate_complexity(files_changed, diff_content)
        metrics['coherence_score'] = self._calculate_coherence(metrics)
        
        return metrics
    
    def _count_lines(self, diff_content: str) -> int:
        """Cuenta líneas agregadas/modificadas en el diff"""
        lines = diff_content.split('\n')
        added_lines = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
        return added_lines
    
    def _is_sacred_core(self, file_path: str) -> bool:
        """Verifica si un archivo es parte del núcleo sagrado"""
        return any(sacred in file_path for sacred in self.sacred_core)
    
    def _analyze_vocabulary(self, diff_content: str) -> Tuple[List[str], List[str]]:
        """
        Analiza uso correcto del vocabulario F3
        
        Returns:
            Tuple de (vocabulary_issues, forbidden_terms)
        """
        vocabulary_issues = []
        forbidden_terms = []
        
        diff_lower = diff_content.lower()
        
        # Buscar términos prohibidos
        for term in self.forbidden_terms:
            if term.lower() in diff_lower:
                # Verificar contexto (no todos los usos son malos)
                if self._is_inappropriate_use(diff_content, term):
                    forbidden_terms.append(term)
        
        # Verificar uso correcto de vocabulario F3
        # (esto es más complejo y requeriría análisis semántico)
        
        return vocabulary_issues, forbidden_terms
    
    def _is_inappropriate_use(self, content: str, term: str) -> bool:
        """
        Verifica si el uso de un término es inapropiado
        (versus uso legítimo en comentarios o strings)
        """
        # Buscar el término en contexto de código (no en strings)
        pattern = rf'\b{re.escape(term)}\b'
        matches = re.finditer(pattern, content, re.IGNORECASE)
        
        for match in matches:
            # Verificar si está en un string literal
            before = content[:match.start()]
            # Contar comillas antes del match
            quotes_before = before.count('"') + before.count("'")
            # Si es par, no está en string
            if quotes_before % 2 == 0:
                return True
        
        return False
    
    def _calculate_complexity(self, files_changed: List[Dict], diff_content: str) -> int:
        """
        Calcula score de complejidad (0-100, mayor = más complejo)
        """
        score = 0
        
        # Más archivos = más complejo
        score += len(files_changed) * 5
        
        # Más líneas = más complejo
        lines = self._count_lines(diff_content)
        score += min(lines // 10, 50)
        
        # Cambios en núcleo sagrado = más complejo
        if any(self._is_sacred_core(f.get('filename', '')) for f in files_changed):
            score += 30
        
        return min(score, 100)
    
    def _calculate_coherence(self, metrics: Dict) -> int:
        """
        Calcula score de coherencia con modelo F3 (0-100, mayor = más coherente)
        """
        score = 100
        
        # Penalizar por términos prohibidos
        score -= len(metrics['forbidden_terms_found']) * 20
        
        # Penalizar por problemas de vocabulario
        score -= len(metrics['vocabulary_issues']) * 10
        
        # Penalizar por tamaño excesivo
        if not metrics['size_ok']:
            score -= 30
        
        return max(score, 0)
    
    def get_analysis_summary(self, metrics: Dict) -> str:
        """Genera resumen legible del análisis"""
        summary = []
        summary.append(f"📊 Análisis del PR:")
        summary.append(f"  - Líneas: {metrics['total_lines']}")
        summary.append(f"  - Archivos: {metrics['files_affected']}")
        summary.append(f"  - Complejidad: {metrics['complexity_score']}/100")
        summary.append(f"  - Coherencia F3: {metrics['coherence_score']}/100")
        
        if metrics['touches_sacred_core']:
            summary.append("  ⚠️  Toca núcleo sagrado (requiere discusión previa)")
        
        if not metrics['size_ok']:
            summary.append(f"  ⚠️  PR muy grande (máximo: {self.max_pr_size} líneas)")
        
        if metrics['forbidden_terms_found']:
            summary.append(f"  ⚠️  Términos prohibidos encontrados: {', '.join(metrics['forbidden_terms_found'])}")
        
        return '\n'.join(summary)

