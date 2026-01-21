"""
Development Phase - Equivalente al SystemPhase del kernel

El agente opera en el mismo ciclo que el kernel:
Lógico → Ilógico → Síntesis → Perfecto
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class DevelopmentPhase(Enum):
    """Fases del ciclo de desarrollo adaptativo"""
    LOGICAL = "logical"      # Desarrollo estable, código ordenado
    ILLOGICAL = "illogical"  # Exploración, ideas nuevas
    SYNTHESIS = "synthesis"  # Evaluación, síntesis de ideas
    PERFECT = "perfect"       # Optimización, aplicación de mejores prácticas


@dataclass
class DevelopmentState:
    """Estado del ciclo de desarrollo"""
    phase: DevelopmentPhase
    entropy: int  # 0-255: medida de caos/exploración
    perfection_score: int  # -32768 a 32767: calidad del proyecto
    cycle_count: int  # Contador de ciclos completados
    prs_processed_in_phase: int  # PRs procesados en fase actual
    
    def __post_init__(self):
        if not 0 <= self.entropy <= 255:
            raise ValueError("Entropy must be between 0 and 255")
        if not -32768 <= self.perfection_score <= 32767:
            raise ValueError("Perfection score must be between -32768 and 32767")


class DevelopmentCycle:
    """Gestiona el ciclo de desarrollo adaptativo"""
    
    def __init__(self, config: dict):
        self.config = config
        self.state = DevelopmentState(
            phase=DevelopmentPhase.LOGICAL,
            entropy=0,
            perfection_score=0,
            cycle_count=0,
            prs_processed_in_phase=0
        )
        self._load_phase_durations()
    
    def _load_phase_durations(self):
        """Carga duraciones de fases desde configuración"""
        cycle_config = self.config.get('development_cycle', {})
        self.phase_durations = {
            DevelopmentPhase.LOGICAL: cycle_config.get('logical_phase_duration', 10),
            DevelopmentPhase.ILLOGICAL: cycle_config.get('illogical_phase_duration', 5),
            DevelopmentPhase.SYNTHESIS: cycle_config.get('synthesis_phase_duration', 3),
            DevelopmentPhase.PERFECT: cycle_config.get('perfect_phase_duration', 8),
        }
        self.entropy_threshold = cycle_config.get('entropy_threshold', 200)
        self.illogical_entropy_start = cycle_config.get('illogical_entropy_start', 100)
    
    def process_pr(self, pr_result: dict) -> None:
        """Procesa un PR y actualiza el estado del ciclo"""
        self.state.prs_processed_in_phase += 1
        
        # Actualizar perfection_score basado en resultado del PR
        if pr_result.get('approved', False):
            self.state.perfection_score += 10
        else:
            self.state.perfection_score -= 5
        
        # Actualizar entropía según fase
        self._update_entropy(pr_result)
        
        # Verificar transiciones
        self._check_transitions()
    
    def _update_entropy(self, pr_result: dict) -> None:
        """Actualiza entropía según fase actual"""
        if self.state.phase == DevelopmentPhase.LOGICAL:
            # En fase lógica, entropía se mantiene baja
            self.state.entropy = max(0, self.state.entropy - 1)
        
        elif self.state.phase == DevelopmentPhase.ILLOGICAL:
            # En fase ilógica, entropía crece (exploración)
            if pr_result.get('experimental', False):
                self.state.entropy = min(255, self.state.entropy + 10)
            else:
                self.state.entropy = min(255, self.state.entropy + 5)
        
        elif self.state.phase == DevelopmentPhase.SYNTHESIS:
            # En síntesis, entropía disminuye (orden emerge)
            self.state.entropy = max(0, self.state.entropy - 20)
        
        elif self.state.phase == DevelopmentPhase.PERFECT:
            # En perfecto, entropía se mantiene baja
            self.state.entropy = max(0, self.state.entropy - 2)
    
    def _check_transitions(self) -> None:
        """Verifica y ejecuta transiciones entre fases"""
        current_phase = self.state.phase
        prs_in_phase = self.state.prs_processed_in_phase
        duration = self.phase_durations[current_phase]
        
        # Transiciones basadas en duración de fase
        if prs_in_phase >= duration:
            if current_phase == DevelopmentPhase.LOGICAL:
                self._transition_to_illogical()
            elif current_phase == DevelopmentPhase.ILLOGICAL:
                if self.state.entropy >= self.entropy_threshold:
                    self._transition_to_synthesis()
            elif current_phase == DevelopmentPhase.SYNTHESIS:
                if self.state.entropy < 50:
                    self._transition_to_perfect()
            elif current_phase == DevelopmentPhase.PERFECT:
                self._transition_to_logical()
    
    def _transition_to_illogical(self) -> None:
        """Transición: LÓGICO → ILÓGICO"""
        self.state.phase = DevelopmentPhase.ILLOGICAL
        self.state.entropy = self.illogical_entropy_start
        self.state.prs_processed_in_phase = 0
        print(f"[CICLO] Transición: LÓGICO → ILÓGICO (entropía: {self.state.entropy})")
    
    def _transition_to_synthesis(self) -> None:
        """Transición: ILÓGICO → SÍNTESIS"""
        self.state.phase = DevelopmentPhase.SYNTHESIS
        self.state.prs_processed_in_phase = 0
        print(f"[CICLO] Transición: ILÓGICO → SÍNTESIS (entropía: {self.state.entropy})")
    
    def _transition_to_perfect(self) -> None:
        """Transición: SÍNTESIS → PERFECTO"""
        self.state.phase = DevelopmentPhase.PERFECT
        self.state.prs_processed_in_phase = 0
        print(f"[CICLO] Transición: SÍNTESIS → PERFECTO (score: {self.state.perfection_score})")
    
    def _transition_to_logical(self) -> None:
        """Transición: PERFECTO → LÓGICO (mejorado)"""
        self.state.phase = DevelopmentPhase.LOGICAL
        self.state.entropy = 0
        self.state.cycle_count += 1
        self.state.prs_processed_in_phase = 0
        print(f"[CICLO] Transición: PERFECTO → LÓGICO (ciclo {self.state.cycle_count}, score: {self.state.perfection_score})")
    
    def get_current_phase(self) -> DevelopmentPhase:
        """Obtiene la fase actual"""
        return self.state.phase
    
    def get_state(self) -> DevelopmentState:
        """Obtiene el estado completo"""
        return self.state
    
    def should_allow_experimentation(self) -> bool:
        """Determina si se permite experimentación (fase ilógica)"""
        return self.state.phase == DevelopmentPhase.ILLOGICAL
    
    def should_enforce_strictness(self) -> bool:
        """Determina si se debe ser estricto (fase lógica o perfecta)"""
        return self.state.phase in (DevelopmentPhase.LOGICAL, DevelopmentPhase.PERFECT)


