"""
Autonomous Executor - Ejecutor Autónomo del Agente

Permite al agente ejecutar código, crear archivos, implementar features
y completar tareas del proyecto de forma 100% autónoma.
"""

import os
import subprocess
import logging
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class AutonomousExecutor:
    """Ejecutor autónomo que permite al agente implementar código automáticamente"""
    
    def __init__(self, project_root: Path, agent_rules, resource_manager):
        self.project_root = Path(project_root)
        self.agent_rules = agent_rules
        self.resource_manager = resource_manager
        self.execution_history: List[Dict] = []
        
        logger.info("✅ Ejecutor autónomo inicializado - El agente puede implementar código automáticamente")
    
    def can_execute(self, action: str, context: Dict) -> Tuple[bool, Optional[str]]:
        """Verifica si puede ejecutar una acción"""
        # Verificar reglas
        is_allowed, blocking_rule = self.agent_rules.is_allowed(action, context)
        
        if not is_allowed:
            return False, f"Bloqueado por regla: {blocking_rule.title if blocking_rule else 'desconocida'}"
        
        # Verificar recursos
        stats = self.resource_manager.get_resource_stats()
        if not stats.get('within_limits', True):
            return False, "Recursos fuera de límites"
        
        return True, None
    
    def create_file(self, file_path: str, content: str, context: Dict = None) -> Dict:
        """Crea un archivo en el proyecto"""
        full_path = self.project_root / file_path
        
        # Verificar permisos
        can_exec, reason = self.can_execute("create_file", {
            'file_path': str(full_path),
            'type': 'file_creation',
            **(context or {})
        })
        
        if not can_exec:
            return {
                'success': False,
                'error': reason,
                'file_path': file_path
            }
        
        try:
            # Registrar actividad
            from .activity_stream import log_file_create
            activity = log_file_create(file_path)
            start_time = time.time()
            
            # Crear directorio si no existe
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Escribir archivo
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Actualizar actividad
            from .activity_stream import get_activity_stream
            stream = get_activity_stream()
            stream.update_activity(activity.id, status="success",
                                 description=f"Archivo creado ({len(content)} bytes)",
                                 duration_ms=duration_ms)
            
            # Registrar ejecución
            execution = {
                'timestamp': datetime.now().isoformat(),
                'action': 'create_file',
                'file_path': file_path,
                'success': True
            }
            self.execution_history.append(execution)
            
            logger.info(f"✅ Archivo creado: {file_path}")
            
            return {
                'success': True,
                'file_path': file_path,
                'size': len(content)
            }
            
        except Exception as e:
            logger.error(f"❌ Error creando archivo {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    def modify_file(self, file_path: str, modifications: List[Dict], context: Dict = None) -> Dict:
        """Modifica un archivo existente
        
        modifications: Lista de modificaciones
        [
            {'type': 'replace', 'old': 'old_text', 'new': 'new_text'},
            {'type': 'insert', 'after': 'marker', 'content': 'new_content'},
            {'type': 'delete', 'text': 'text_to_delete'}
        ]
        """
        full_path = self.project_root / file_path
        
        # Verificar permisos
        can_exec, reason = self.can_execute("modify_file", {
            'file_path': str(full_path),
            'type': 'code_modification',
            'modified_files': [file_path],
            **(context or {})
        })
        
        if not can_exec:
            return {
                'success': False,
                'error': reason,
                'file_path': file_path
            }
        
        try:
            # Registrar actividad
            from .activity_stream import log_file_modify
            activity = log_file_modify(file_path, len(modifications))
            start_time = time.time()
            
            # Leer archivo actual
            if not full_path.exists():
                from .activity_stream import get_activity_stream
                stream = get_activity_stream()
                stream.update_activity(activity.id, status="error",
                                     description=f"Archivo no existe: {file_path}")
                return {
                    'success': False,
                    'error': f'Archivo no existe: {file_path}',
                    'file_path': file_path
                }
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Aplicar modificaciones
            for mod in modifications:
                if mod['type'] == 'replace':
                    content = content.replace(mod['old'], mod['new'])
                elif mod['type'] == 'insert':
                    marker = mod.get('after', '')
                    if marker in content:
                        content = content.replace(marker, marker + '\n' + mod['content'])
                    else:
                        content += '\n' + mod['content']
                elif mod['type'] == 'delete':
                    content = content.replace(mod['text'], '')
            
            # Escribir archivo modificado
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Actualizar actividad
            from .activity_stream import get_activity_stream
            stream = get_activity_stream()
            stream.update_activity(activity.id, status="success",
                                 description=f"{len(modifications)} cambios aplicados",
                                 duration_ms=duration_ms)
            
            # Registrar ejecución
            execution = {
                'timestamp': datetime.now().isoformat(),
                'action': 'modify_file',
                'file_path': file_path,
                'modifications_count': len(modifications),
                'success': True
            }
            self.execution_history.append(execution)
            
            logger.info(f"✅ Archivo modificado: {file_path} ({len(modifications)} cambios)")
            
            return {
                'success': True,
                'file_path': file_path,
                'modifications_applied': len(modifications)
            }
            
        except Exception as e:
            logger.error(f"❌ Error modificando archivo {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    def execute_command(self, command: List[str], cwd: Optional[str] = None, context: Dict = None) -> Dict:
        """Ejecuta un comando del sistema"""
        # Verificar permisos
        can_exec, reason = self.can_execute("execute_command", {
            'command': ' '.join(command),
            'type': 'system_command',
            **(context or {})
        })
        
        if not can_exec:
            return {
                'success': False,
                'error': reason,
                'command': ' '.join(command)
            }
        
        try:
            # Registrar actividad
            from .activity_stream import log_command_execute
            activity = log_command_execute(' '.join(command))
            start_time = time.time()
            
            # Ejecutar comando
            work_dir = self.project_root / (cwd or '')
            result = subprocess.run(
                command,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos máximo
            )
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Actualizar actividad
            from .activity_stream import get_activity_stream
            stream = get_activity_stream()
            status = "success" if result.returncode == 0 else "error"
            stream.update_activity(activity.id, status=status,
                                 description=f"Código: {result.returncode}",
                                 duration_ms=duration_ms)
            
            # Registrar ejecución
            execution = {
                'timestamp': datetime.now().isoformat(),
                'action': 'execute_command',
                'command': ' '.join(command),
                'return_code': result.returncode,
                'success': result.returncode == 0
            }
            self.execution_history.append(execution)
            
            if result.returncode == 0:
                logger.info(f"✅ Comando ejecutado: {' '.join(command)}")
            else:
                logger.warning(f"⚠️  Comando falló: {' '.join(command)} (código: {result.returncode})")
            
            return {
                'success': result.returncode == 0,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(command)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout (5 minutos)',
                'command': ' '.join(command)
            }
        except Exception as e:
            logger.error(f"❌ Error ejecutando comando {' '.join(command)}: {e}")
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(command)
            }
    
    def build_project(self, context: Dict = None) -> Dict:
        """Compila el proyecto F3-OS"""
        from .activity_stream import log_build
        activity = log_build()
        start_time = time.time()
        
        result = self.execute_command(['./build.sh'], context=context)
        
        duration_ms = int((time.time() - start_time) * 1000)
        from .activity_stream import get_activity_stream
        stream = get_activity_stream()
        stream.update_activity(activity.id, 
                             status="success" if result['success'] else "error",
                             description=f"Compilación {'exitosa' if result['success'] else 'fallida'}",
                             duration_ms=duration_ms)
        
        return result
    
    def run_tests(self, context: Dict = None) -> Dict:
        """Ejecuta tests del proyecto"""
        # Buscar y ejecutar tests
        test_commands = [
            ['cargo', 'test', '--manifest-path', 'kernel/Cargo.toml'],
            ['python3', '-m', 'pytest', 'agent/tests/'] if (self.project_root / 'agent/tests').exists() else None
        ]
        
        results = []
        for cmd in test_commands:
            if cmd:
                result = self.execute_command(cmd, context=context)
                results.append(result)
        
        return {
            'success': all(r['success'] for r in results),
            'results': results
        }
    
    def create_feature(self, feature_name: str, description: str, implementation: Dict, context: Dict = None) -> Dict:
        """Crea una nueva feature completa
        
        implementation: {
            'files': [
                {'path': 'path/to/file.rs', 'content': '...'},
                ...
            ],
            'modifications': [
                {'file': 'existing.rs', 'modifications': [...]},
                ...
            ],
            'tests': [...]
        }
        """
        results = []
        
        # Crear archivos nuevos
        for file_info in implementation.get('files', []):
            result = self.create_file(
                file_info['path'],
                file_info['content'],
                context={**(context or {}), 'feature': feature_name}
            )
            results.append(result)
        
        # Modificar archivos existentes
        for mod_info in implementation.get('modifications', []):
            result = self.modify_file(
                mod_info['file'],
                mod_info['modifications'],
                context={**(context or {}), 'feature': feature_name}
            )
            results.append(result)
        
        # Crear tests
        for test_info in implementation.get('tests', []):
            result = self.create_file(
                test_info['path'],
                test_info['content'],
                context={**(context or {}), 'feature': feature_name, 'type': 'test'}
            )
            results.append(result)
        
        success = all(r.get('success', False) for r in results)
        
        if success:
            logger.info(f"✅ Feature '{feature_name}' creada exitosamente")
        else:
            logger.warning(f"⚠️  Feature '{feature_name}' creada con errores")
        
        return {
            'success': success,
            'feature_name': feature_name,
            'results': results
        }
    
    def get_execution_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Obtiene historial de ejecuciones"""
        if limit:
            return self.execution_history[-limit:]
        return self.execution_history
    
    def save_execution_log(self, file_path: str = "agent/data/execution_log.json"):
        """Guarda el historial de ejecuciones"""
        log_path = self.project_root / file_path
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.execution_history, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Log de ejecuciones guardado: {file_path}")

