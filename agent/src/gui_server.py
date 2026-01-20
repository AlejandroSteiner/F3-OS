"""
GUI Server - Servidor para integración con GUI de F3-OS

Proporciona API HTTP simple para que la GUI del sistema se comunique con el asistente.
"""

import json
from typing import Dict, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

from .gui_integration import GUIIntegration


class AssistantHTTPHandler(BaseHTTPRequestHandler):
    """Handler HTTP para el asistente GUI"""
    
    def __init__(self, gui_integration: GUIIntegration, *args, **kwargs):
        self.gui = gui_integration
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Maneja peticiones GET"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/' or path == '/index.html':
            self._handle_index()
        elif path == '/assistant/status':
            self._handle_status()
        elif path == '/api/status':
            self._handle_api_status()
        elif path == '/assistant/conversation':
            self._handle_conversation()
        elif path == '/assistant/suggestions':
            self._handle_suggestions()
        else:
            self._send_error(404, "Not Found")
    
    def do_POST(self):
        """Maneja peticiones POST"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/assistant/open':
            self._handle_open()
        elif path == '/assistant/close':
            self._handle_close()
        elif path == '/assistant/message' or path == '/api/query':
            self._handle_message()
        else:
            self._send_error(404, "Not Found")
    
    def _handle_index(self):
        """Sirve la página HTML principal"""
        import os
        from pathlib import Path
        
        # Buscar index.html en gui_web/
        script_dir = Path(__file__).parent.parent
        html_path = script_dir / 'gui_web' / 'index.html'
        
        if html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            # HTML básico si no existe el archivo
            html = """
<!DOCTYPE html>
<html>
<head><title>F3-OS Assistant</title></head>
<body>
<h1>F3-OS Assistant</h1>
<p>Servidor funcionando. Abre la consola del navegador para usar la API.</p>
<p>Endpoints disponibles:</p>
<ul>
<li>GET /api/status - Estado del agente</li>
<li>POST /api/query - Enviar consulta</li>
</ul>
</body>
</html>
"""
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
    
    def _handle_api_status(self):
        """Obtiene estado del agente para la API"""
        status = self.gui.governance_core.get_status()
        resources = self.gui.resource_manager.get_stats()
        
        self._send_json(200, {
            'phase': status.get('phase', 'unknown'),
            'entropy': status.get('entropy', 0),
            'perfection_score': status.get('perfection_score', 0),
            'cycle_count': status.get('cycle_count', 0),
            'cpu_percent': resources.get('cpu_percent', 0.0),
            'memory_mb': resources.get('memory_mb', 0.0),
        })
    
    def _handle_status(self):
        """Obtiene estado del asistente"""
        state = self.gui.get_window_state()
        self._send_json(200, state)
    
    def _handle_conversation(self):
        """Obtiene historial de conversación"""
        conversation = self.gui.get_conversation()
        self._send_json(200, {'conversation': conversation})
    
    def _handle_suggestions(self):
        """Obtiene sugerencias"""
        suggestions = self.gui.get_suggestions()
        self._send_json(200, {'suggestions': suggestions})
    
    def _handle_open(self):
        """Abre el asistente"""
        greeting = self.gui.open_assistant()
        self._send_json(200, {'message': greeting, 'opened': True})
    
    def _handle_close(self):
        """Cierra el asistente"""
        self.gui.close_assistant()
        self._send_json(200, {'closed': True})
    
    def _handle_message(self):
        """Envía mensaje al asistente"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self._send_error(400, "Content-Length required")
            return
            
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            # Soporta tanto 'message' como 'query'
            message = data.get('message') or data.get('query', '')
            
            if not message:
                self._send_error(400, "Message or query required")
                return
            
            response = self.gui.send_message(message)
            self._send_json(200, {'response': response})
        
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
        except Exception as e:
            self._send_error(500, str(e))
    
    def _send_json(self, status_code: int, data: Dict):
        """Envía respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Para desarrollo
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def _send_error(self, status_code: int, message: str):
        """Envía error"""
        self._send_json(status_code, {'error': message})
    
    def log_message(self, format, *args):
        """Suprime logs de HTTP server"""
        pass  # No loguear cada petición


class GUIServer:
    """Servidor HTTP para el asistente GUI"""
    
    def __init__(self, gui_integration: GUIIntegration, port: int = 8080):
        self.gui = gui_integration
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self) -> None:
        """Inicia el servidor"""
        if self.running:
            return
        
        def handler_factory(*args, **kwargs):
            return AssistantHTTPHandler(self.gui, *args, **kwargs)
        
        self.server = HTTPServer(('localhost', self.port), handler_factory)
        self.running = True
        
        def run_server():
            print(f"🌐 Servidor GUI del asistente iniciado en http://localhost:{self.port}")
            print(f"📱 Abre en tu navegador: http://localhost:{self.port}")
            print(f"💬 Interfaz web disponible para chatear con el asistente")
            print("")
            while self.running:
                try:
                    self.server.handle_request()
                except Exception as e:
                    if self.running:  # Solo loguear si aún está corriendo
                        print(f"Error en servidor: {e}")
        
        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()
    
    def stop(self) -> None:
        """Detiene el servidor"""
        self.running = False
        if self.server:
            self.server.shutdown()
        if self.server_thread:
            self.server_thread.join(timeout=2.0)
    
    def is_running(self) -> bool:
        """Verifica si el servidor está corriendo"""
        return self.running

