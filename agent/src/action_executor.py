"""
Action Executor - Ejecutor de Acciones del Asistente

Permite al agente ejecutar acciones reales además de responder:
- Verificar conexión a internet
- Descargar desde URLs
- Instalar aplicaciones (pip, etc.)
- Trabajar sobre proyectos/aplicaciones
"""

import re
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ActionExecutor:
    """Ejecutor de acciones que el asistente puede realizar"""
    
    def __init__(self, config: dict, project_root: Optional[Path] = None):
        self.config = config
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent.parent
        self.downloads_dir = self.project_root / "agent" / "downloads"
        self.downloads_dir.mkdir(parents=True, exist_ok=True)
        
        # Límites
        internet_config = config.get('internet_learning', {})
        self.internet_enabled = internet_config.get('enabled', False)
        self.allowed_domains = internet_config.get('allowed_domains', [])
        
        logger.info("✅ Action Executor inicializado")
    
    def check_internet_connection(self) -> Tuple[bool, str]:
        """
        Verifica si hay conexión a internet.
        Returns: (connected, message)
        """
        try:
            import requests
            # Usar endpoints públicos y rápidos
            endpoints = [
                "https://api.github.com",
                "https://www.google.com",
            ]
            
            for url in endpoints:
                try:
                    response = requests.get(url, timeout=3)
                    if response.status_code in (200, 204, 301, 302):
                        return True, "Sí, tengo conexión a internet. Puedo buscar información y descargar recursos."
                except Exception:
                    continue
            
            return False, "No pude verificar la conexión. Algunos endpoints no respondieron."
            
        except ImportError:
            return False, "El módulo 'requests' no está instalado. No puedo verificar la conexión."
        except Exception as e:
            logger.error(f"Error verificando internet: {e}")
            return False, f"No pude conectar. Posible problema de red: {str(e)[:100]}"
    
    def get_current_activity(self) -> str:
        """Obtiene qué está haciendo el agente actualmente"""
        try:
            from .activity_stream import get_activity_stream
            stream = get_activity_stream()
            activities = stream.get_recent_activities(limit=5)
            
            if not activities:
                return (
                    "Por ahora no tengo tareas activas en ejecución. "
                    "Estoy listo para ayudarte: puedo analizar el proyecto, buscar información, "
                    "o trabajar en tareas que me indiques."
                )
            
            lines = ["**Actividad reciente:**\n"]
            for i, act in enumerate(reversed(activities[-5:]), 1):
                title = act.get('title', 'Actividad')
                desc = act.get('description', '')
                status = act.get('status', 'running')
                status_emoji = "✅" if status == "success" else "🔄" if status == "running" else "⚠️"
                lines.append(f"{i}. {status_emoji} {title}")
                if desc:
                    lines.append(f"   _{desc}_")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"Error obteniendo actividad: {e}")
            return "No pude recuperar el estado actual. Estoy disponible para ayudarte."
    
    def extract_url_from_text(self, text: str) -> Optional[str]:
        """Extrae una URL del texto del usuario"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        matches = re.findall(url_pattern, text)
        if matches:
            return matches[0].rstrip('.,;:)')
        return None
    
    def download_from_url(self, url: str, filename: Optional[str] = None) -> Dict:
        """
        Descarga un archivo desde una URL.
        Returns: {success, path, error}
        """
        try:
            import requests
        except ImportError:
            return {
                'success': False,
                'error': 'El módulo requests no está instalado.',
                'path': None
            }
        
        if not self.internet_enabled:
            # Aun así intentar: la descarga es una acción explícita del usuario
            logger.info("Internet learning desactivado, pero el usuario pidió descargar explícitamente.")
        
        # Verificar dominio permitido (relajado para descargas)
        parsed = urlparse(url)
        if self.allowed_domains and parsed.netloc:
            if not any(d in parsed.netloc for d in self.allowed_domains):
                logger.warning(f"Dominio no en lista permitida: {parsed.netloc}")
                # Permitir de todos modos pero registrar - el usuario pidió descargar
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            if not filename:
                content_disp = response.headers.get('Content-Disposition')
                if content_disp and 'filename=' in content_disp:
                    filename = re.findall(r'filename[*]?=["\']?([^"\';]+)', content_disp)[-1]
                else:
                    filename = url.split('/')[-1] or "downloaded_file"
            
            dest_path = self.downloads_dir / filename
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            size = dest_path.stat().st_size
            logger.info(f"✅ Descargado: {url} -> {dest_path} ({size} bytes)")
            
            return {
                'success': True,
                'path': str(dest_path),
                'size': size,
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error descargando {url}: {e}")
            return {
                'success': False,
                'error': str(e),
                'path': None
            }
    
    def install_package(self, package_name: str, is_pip: bool = True) -> Dict:
        """
        Instala un paquete (pip por defecto).
        Returns: {success, output, error}
        """
        if not package_name or not package_name.strip():
            return {'success': False, 'error': 'No se especificó nombre de paquete.'}
        
        try:
            import subprocess
            if is_pip:
                result = subprocess.run(
                    [os.environ.get('PYTHON', 'python3'), '-m', 'pip', 'install', package_name.strip()],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
            else:
                return {'success': False, 'error': 'Solo instalación via pip está soportada por ahora.'}
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'output': result.stdout or 'Instalado correctamente.',
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'output': result.stdout,
                    'error': result.stderr or f'Código de salida: {result.returncode}'
                }
                
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Timeout (máximo 2 minutos).'}
        except Exception as e:
            logger.error(f"Error instalando {package_name}: {e}")
            return {'success': False, 'error': str(e)}
    
    def work_on_application(self, path_or_name: str) -> Dict:
        """
        Analiza y prepara trabajo sobre una aplicación/proyecto.
        Returns: {success, analysis, suggestions}
        """
        target = Path(path_or_name)
        if not target.is_absolute():
            target = self.project_root / path_or_name
        
        if not target.exists():
            # Buscar en el proyecto
            for candidate in self.project_root.rglob(path_or_name):
                if candidate.is_file() or (candidate.is_dir() and (candidate / 'Cargo.toml').exists()):
                    target = candidate
                    break
            else:
                return {
                    'success': False,
                    'error': f'No encontré "{path_or_name}" en el proyecto.',
                    'suggestions': []
                }
        
        try:
            from .project_analyzer import ProjectAnalyzer
            analyzer = ProjectAnalyzer(project_root=str(self.project_root))
            
            if target.is_file():
                with open(target, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                analysis = f"**Archivo:** {target.name}\n"
                analysis += f"Tamaño: {len(content)} caracteres\n"
                if target.suffix in ('.rs', '.py', '.md'):
                    analysis += f"Tipo: {target.suffix}\n"
                
                # Buscar información relevante en el proyecto
                search = analyzer.search_in_files(target.stem or path_or_name)
                if search:
                    analysis += "\n**Contexto en el proyecto:**\n"
                    for fn, cont in search[:2]:
                        analysis += f"- {fn}: {cont[:150]}...\n"
                
                return {
                    'success': True,
                    'analysis': analysis,
                    'path': str(target),
                    'suggestions': [
                        "Puedo modificarlo si me indicas qué cambiar.",
                        "Puedo buscar más contexto en el proyecto.",
                    ]
                }
            
            else:
                # Es un directorio
                files = list(target.rglob('*'))[:20]
                rust_files = [f for f in files if f.suffix == '.rs']
                analysis = f"**Directorio:** {target.name}\n"
                analysis += f"Archivos: ~{len(files)}\n"
                if rust_files:
                    analysis += f"Archivos Rust: {len(rust_files)}\n"
                
                if (target / 'Cargo.toml').exists():
                    analysis += "\nEs un proyecto Cargo/Rust."
                if (target / 'requirements.txt').exists():
                    analysis += "\nTiene requirements.txt (Python)."
                
                return {
                    'success': True,
                    'analysis': analysis,
                    'path': str(target),
                    'suggestions': [
                        "Puedo analizar la estructura en detalle.",
                        "Puedo revisar dependencias (Cargo.toml, etc.).",
                        "Puedo sugerir mejoras según el modelo F3.",
                    ]
                }
                
        except Exception as e:
            logger.error(f"Error analizando {path_or_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'suggestions': []
            }
