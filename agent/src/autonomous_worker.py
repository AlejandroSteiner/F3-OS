"""
Autonomous Worker - Trabajador Autónomo del Agente

Ejecuta tareas automáticamente en segundo plano para completar el proyecto.
"""

import time
import threading
import logging
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AutonomousWorker:
    """Trabajador autónomo que ejecuta tareas periódicamente"""
    
    def __init__(self, governance_core, config: Dict):
        self.governance_core = governance_core
        self.config = config
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.work_interval = config.get('autonomous_worker', {}).get('work_interval', 30)  # 30 segundos
        
        logger.info("✅ Trabajador autónomo inicializado")
    
    def start(self):
        """Inicia el trabajador autónomo"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._work_loop, daemon=True)
        self.worker_thread.start()
        
        from .activity_stream import log_success
        log_success("Trabajador autónomo iniciado - Ejecutando tareas periódicamente")
        
        logger.info("✅ Trabajador autónomo iniciado")
    
    def stop(self):
        """Detiene el trabajador autónomo"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        logger.info("🛑 Trabajador autónomo detenido")
    
    def _work_loop(self):
        """Loop principal del trabajador"""
        while self.running:
            try:
                # Ejecutar ciclo de trabajo
                self._execute_work_cycle()
                
                # Esperar antes del siguiente ciclo
                time.sleep(self.work_interval)
                
            except Exception as e:
                logger.error(f"Error en ciclo de trabajo: {e}")
                from .activity_stream import log_error
                log_error(f"Error en ciclo de trabajo: {e}")
                time.sleep(self.work_interval)
    
    def _execute_work_cycle(self):
        """Ejecuta un ciclo de trabajo"""
        from .activity_stream import log_thinking, log_decision
        
        # 1. Analizar estado del proyecto
        log_thinking("Analizando estado del proyecto F3-OS...")
        
        # 2. Verificar si hay tareas pendientes
        # (Por ahora, solo registramos que está trabajando)
        
        # 3. Monitorear recursos
        stats = self.governance_core.resource_manager.get_resource_stats()
        if stats.get('within_limits', True):
            # El agente está operando correctamente
            pass
        else:
            log_error("Recursos fuera de límites")
        
        # 4. Verificar estado del ciclo de desarrollo
        phase_state = self.governance_core.development_cycle.get_state()
        log_decision(f"Fase actual: {phase_state.phase.value.upper()}", 
                    f"Entropía: {phase_state.entropy}/255, Perfección: {phase_state.perfection_score}")
        
        # 5. Verificar si hay conocimiento nuevo para aprender
        # (Esto se puede expandir más adelante)


