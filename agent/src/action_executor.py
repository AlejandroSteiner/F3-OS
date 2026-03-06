"""
Action Executor - Ejecutor de Acciones del Asistente

Permite al agente ejecutar acciones reales además de responder:
- Verificar conexión a internet
- Descargar desde URLs
- Instalar aplicaciones (pip, etc.)
- Trabajar sobre proyectos/aplicaciones
"""

import html
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
    
    def construct_url_from_query(self, text: str) -> Optional[str]:
        """
        Construye URL cuando el usuario dice "entra a X" o "busca en X".
        Ej: "dolarbluehoy salta" → https://dolarhoy.com/dolar-blue-salta
        """
        text_lower = text.lower()
        # Sitios conocidos de cotización argentina
        if 'dolarbluehoy' in text_lower or 'dolar blue' in text_lower or 'dolarblue' in text_lower:
            # dolarbluehoy.com está parked; usar dolarhoy.com (cotización nacional)
            return 'https://dolarhoy.com'
        if 'dolarhoy' in text_lower:
            return 'https://dolarhoy.com'
        if 'ambito' in text_lower:
            return 'https://www.ambito.com/contenidos/dolar.html'
        # Buscar patrones "entra a SITIO" o "busca en SITIO"
        for prefix in ['entra a ', 'entrá a ', 'busca en ', 've a ', 'accede a ']:
            if prefix in text_lower:
                rest = text.split(prefix, 1)[-1].split(' y ')[0].strip()
                words = re.findall(r'[\w\.]+', rest)
                if words:
                    site = words[0].replace(' ', '')
                    if '.' not in site:
                        site += '.com'
                    if not site.startswith('http'):
                        return f'https://{site}'
                break
        return None
    
    def fetch_web_page(self, url: str) -> Dict:
        """
        Obtiene contenido de una página web.
        Returns: {success, content, title, error}
        """
        try:
            import requests
        except ImportError:
            return {'success': False, 'content': '', 'error': 'Módulo requests no instalado.'}
        
        try:
            response = requests.get(
                url,
                timeout=15,
                headers={'User-Agent': 'F3-OS-Agent/1.0 (Assistant)'}
            )
            response.raise_for_status()
            
            # Extraer texto
            html = response.text
            text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            text = html.unescape(text)
            
            title = ''
            if '<title' in html.lower():
                m = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
                if m:
                    title = re.sub(r'<[^>]+>', '', m.group(1)).strip()[:200]
            
            return {
                'success': True,
                'content': text[:15000],  # Limitar tamaño
                'title': title,
                'url': url,
                'error': None
            }
        except Exception as e:
            logger.error(f"Error fetch {url}: {e}")
            return {
                'success': False,
                'content': '',
                'title': '',
                'error': str(e)[:200]
            }
    
    def extract_data_from_content(self, content: str, query: str) -> str:
        """
        Extrae datos relevantes del contenido según la consulta.
        Para "dolar blue", "cotización", busca precios.
        """
        content_lower = content.lower()
        query_lower = query.lower()
        results = []
        
        # Patrones de precios (Argentina: 1.234,56 o $1234)
        price_patterns = [
            r'\$\s*[\d\.,]+',           # $1.234,56
            r'[\d\.,]+\s*pesos',        # 1234 pesos
            r'[\d\.,]+\s*ars',           # 1234 ARS
            r'(?:compra|venta)\s*:?\s*[\d\.,]+',
            r'(?:compra|venta)\s*[\$]?\s*[\d\.,]+',
        ]
        
        if 'dolar' in query_lower or 'blue' in query_lower or 'cotización' in query_lower or 'cotizacion' in query_lower:
            for pat in price_patterns:
                for m in re.finditer(pat, content_lower, re.IGNORECASE):
                    snippet = content[max(0, m.start()-50):m.end()+80]
                    if snippet not in results:
                        results.append(snippet.strip())
            
            # Buscar contexto "blue", "compra", "venta"
            for keyword in ['blue', 'compra', 'venta', 'dólar', 'dolar']:
                idx = content_lower.find(keyword)
                if idx >= 0:
                    snippet = content[max(0, idx-20):idx+150]
                    if len(snippet) > 30 and snippet not in results:
                        results.append(snippet.strip())
        
        if results:
            return '\n\n'.join(results[:8])[:2000]
        
        # Fallback: devolver fragmentos que contengan términos de la query
        words = set(re.findall(r'\w+', query_lower))
        words.discard('entra')
        words.discard('dime')
        words.discard('la')
        words.discard('de')
        words.discard('en')
        words.discard('frente')
        words.discard('al')
        words.discard('peso')
        words.discard('pesos')
        words.discard('argentino')
        
        for word in list(words)[:3]:
            if len(word) < 4:
                continue
            idx = content_lower.find(word)
            if idx >= 0:
                snippet = content[max(0, idx-30):idx+200]
                if len(snippet) > 20:
                    results.append(snippet.strip())
        
        return '\n\n'.join(results[:5])[:1500] if results else content[:1000]
    
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
