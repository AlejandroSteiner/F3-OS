"""
Context Manager - Equivalente a RAM Thread

Mantiene contexto del proyecto y recuerda decisiones pasadas.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ContextManager:
    """Gestiona contexto y memoria del proyecto"""
    
    def __init__(self, config: dict, data_dir: Path):
        self.config = config
        self.data_dir = data_dir
        self.context_file = data_dir / 'context.json'
        self.decisions_file = data_dir / 'decisions.json'
        self.context = self._load_context()
        self.decisions = self._load_decisions()
    
    def _load_context(self) -> Dict:
        """Carga contexto del proyecto"""
        if self.context_file.exists():
            try:
                with open(self.context_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'project_state': 'initial',
            'last_pr_number': 0,
            'total_prs_processed': 0,
            'accepted_prs': 0,
            'rejected_prs': 0,
            'known_patterns': [],
            'recent_changes': []
        }
    
    def _load_decisions(self) -> List[Dict]:
        """Carga historial de decisiones"""
        if self.decisions_file.exists():
            try:
                with open(self.decisions_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _save_context(self) -> None:
        """Guarda contexto del proyecto"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.context_file, 'w') as f:
            json.dump(self.context, f, indent=2)
    
    def _save_decisions(self) -> None:
        """Guarda historial de decisiones"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with open(self.decisions_file, 'w') as f:
            json.dump(self.decisions, f, indent=2)
    
    def record_decision(self, pr_number: int, decision: str, reason: str, metrics: Dict) -> None:
        """Registra una decisión sobre un PR"""
        decision_record = {
            'pr_number': pr_number,
            'decision': decision,  # 'approved', 'rejected', 'changes_requested'
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
        }
        self.decisions.append(decision_record)
        
        # Actualizar contexto
        self.context['last_pr_number'] = pr_number
        self.context['total_prs_processed'] += 1
        
        if decision == 'approved':
            self.context['accepted_prs'] += 1
        elif decision == 'rejected':
            self.context['rejected_prs'] += 1
        
        # Mantener solo decisiones recientes en contexto
        self.context['recent_changes'].append({
            'pr': pr_number,
            'decision': decision,
            'timestamp': decision_record['timestamp']
        })
        # Mantener solo últimos 20 cambios
        if len(self.context['recent_changes']) > 20:
            self.context['recent_changes'] = self.context['recent_changes'][-20:]
        
        self._save_context()
        self._save_decisions()
    
    def get_similar_decisions(self, metrics: Dict, limit: int = 5) -> List[Dict]:
        """Busca decisiones similares en el historial"""
        similar = []
        
        for decision in reversed(self.decisions[-50:]):  # Buscar en últimos 50
            similarity = self._calculate_similarity(metrics, decision.get('metrics', {}))
            if similarity > 0.5:  # Umbral de similitud
                similar.append({
                    'decision': decision,
                    'similarity': similarity
                })
        
        # Ordenar por similitud y limitar
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar[:limit]
    
    def _calculate_similarity(self, metrics1: Dict, metrics2: Dict) -> float:
        """Calcula similitud entre dos sets de métricas"""
        if not metrics2:
            return 0.0
        
        # Comparar métricas clave
        similarities = []
        
        # Tamaño similar
        size1 = metrics1.get('total_lines', 0)
        size2 = metrics2.get('total_lines', 0)
        if size1 > 0 and size2 > 0:
            size_sim = 1.0 - abs(size1 - size2) / max(size1, size2)
            similarities.append(size_sim)
        
        # Mismo tipo de archivos
        files1 = set(metrics1.get('files_affected', []))
        files2 = set(metrics2.get('files_affected', []))
        if files1 or files2:
            file_sim = len(files1 & files2) / max(len(files1 | files2), 1)
            similarities.append(file_sim)
        
        # Mismo tipo de cambio (núcleo sagrado)
        sacred1 = metrics1.get('touches_sacred_core', False)
        sacred2 = metrics2.get('touches_sacred_core', False)
        if sacred1 == sacred2:
            similarities.append(1.0)
        else:
            similarities.append(0.0)
        
        return sum(similarities) / len(similarities) if similarities else 0.0
    
    def get_context_summary(self) -> str:
        """Genera resumen del contexto actual"""
        summary = []
        summary.append("📚 Contexto del Proyecto:")
        summary.append(f"  - PRs procesados: {self.context['total_prs_processed']}")
        summary.append(f"  - Aceptados: {self.context['accepted_prs']}")
        summary.append(f"  - Rechazados: {self.context['rejected_prs']}")
        summary.append(f"  - Último PR: #{self.context['last_pr_number']}")
        
        if self.context['recent_changes']:
            summary.append("\n  Cambios recientes:")
            for change in self.context['recent_changes'][-5:]:
                summary.append(f"    - PR #{change['pr']}: {change['decision']}")
        
        return '\n'.join(summary)
    
    def update_project_state(self, state: str) -> None:
        """Actualiza el estado del proyecto"""
        self.context['project_state'] = state
        self._save_context()




