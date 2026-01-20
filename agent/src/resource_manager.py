"""
Resource Manager - Gestiona límites de recursos del agente

El agente debe consumir solo 15-20% de CPU para no sobrecargar el sistema.
"""

import time
import psutil
import threading
from typing import Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ResourceLimits:
    """Límites de recursos del agente"""
    max_cpu_percent: float = 20.0  # Máximo 20% de CPU
    target_cpu_percent: float = 15.0  # Objetivo 15% de CPU
    check_interval: float = 1.0  # Verificar cada segundo
    sleep_duration: float = 0.1  # Dormir entre operaciones


class ResourceManager:
    """Gestiona y monitorea uso de recursos del agente"""
    
    def __init__(self, config: dict):
        self.config = config
        resource_config = config.get('resources', {})
        
        self.limits = ResourceLimits(
            max_cpu_percent=resource_config.get('max_cpu_percent', 20.0),
            target_cpu_percent=resource_config.get('target_cpu_percent', 15.0),
            check_interval=resource_config.get('check_interval', 1.0),
            sleep_duration=resource_config.get('sleep_duration', 0.1),
        )
        
        self.process = psutil.Process()
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.current_cpu_usage = 0.0
        self.operation_count = 0
        self.last_check = datetime.now()
    
    def start_monitoring(self) -> None:
        """Inicia monitoreo de recursos en background"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self.monitor_thread.start()
        print(f"📊 Monitoreo de recursos iniciado (límite: {self.limits.max_cpu_percent}% CPU)")
    
    def stop_monitoring(self) -> None:
        """Detiene monitoreo de recursos"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
    
    def _monitor_resources(self) -> None:
        """Monitorea uso de recursos en background"""
        while self.monitoring:
            try:
                # Obtener uso de CPU del proceso actual
                cpu_percent = self.process.cpu_percent(interval=0.1)
                self.current_cpu_usage = cpu_percent
                
                # Si excede el límite, registrar advertencia
                if cpu_percent > self.limits.max_cpu_percent:
                    print(f"⚠️  Uso de CPU alto: {cpu_percent:.1f}% (límite: {self.limits.max_cpu_percent}%)")
                
                time.sleep(self.limits.check_interval)
            except Exception as e:
                print(f"Error en monitoreo de recursos: {e}")
                time.sleep(self.limits.check_interval)
    
    def check_and_throttle(self) -> None:
        """Verifica uso de recursos y aplica throttling si es necesario"""
        current_cpu = self.process.cpu_percent(interval=0.1)
        
        # Si estamos por encima del objetivo, aplicar throttling
        if current_cpu > self.limits.target_cpu_percent:
            # Calcular tiempo de espera proporcional al exceso
            excess = current_cpu - self.limits.target_cpu_percent
            sleep_time = self.limits.sleep_duration * (1 + excess / 10)
            time.sleep(sleep_time)
    
    def rate_limit_operation(self) -> None:
        """Aplica rate limiting entre operaciones"""
        # Dormir entre operaciones para mantener uso bajo
        time.sleep(self.limits.sleep_duration)
        
        # Verificar y aplicar throttling si es necesario
        self.check_and_throttle()
        
        self.operation_count += 1
    
    def get_resource_stats(self) -> dict:
        """Obtiene estadísticas de uso de recursos"""
        try:
            cpu_percent = self.process.cpu_percent(interval=0.1)
            memory_info = self.process.memory_info()
            
            return {
                'cpu_percent': cpu_percent,
                'memory_mb': memory_info.rss / 1024 / 1024,
                'operations': self.operation_count,
                'within_limits': cpu_percent <= self.limits.max_cpu_percent,
                'target_met': cpu_percent <= self.limits.target_cpu_percent,
            }
        except Exception as e:
            return {
                'error': str(e),
                'operations': self.operation_count,
            }
    
    def print_resource_stats(self) -> None:
        """Imprime estadísticas de recursos"""
        stats = self.get_resource_stats()
        if 'error' in stats:
            print(f"⚠️  Error obteniendo stats: {stats['error']}")
            return
        
        status = "✅" if stats['within_limits'] else "⚠️"
        target_status = "✅" if stats['target_met'] else "⚠️"
        
        print(f"\n{status} Recursos del Agente:")
        print(f"  CPU: {stats['cpu_percent']:.1f}% (límite: {self.limits.max_cpu_percent}%)")
        print(f"  {target_status} Objetivo: {stats['cpu_percent']:.1f}% (target: {self.limits.target_cpu_percent}%)")
        print(f"  Memoria: {stats['memory_mb']:.1f} MB")
        print(f"  Operaciones: {stats['operations']}")


class ThrottledOperation:
    """Context manager para operaciones con throttling automático"""
    
    def __init__(self, resource_manager: ResourceManager):
        self.resource_manager = resource_manager
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Aplicar rate limiting después de la operación
        self.resource_manager.rate_limit_operation()
        
        # Si la operación fue muy rápida, esperar un poco más
        elapsed = time.time() - self.start_time
        if elapsed < self.resource_manager.limits.sleep_duration:
            time.sleep(self.resource_manager.limits.sleep_duration - elapsed)

