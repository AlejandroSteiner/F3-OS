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
        
        if path == '/assistant/status':
            self._handle_status()
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
        elif path == '/assistant/message':
            self._handle_message()
        else:
            self._send_error(404, "Not Found")
    
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            
            if not message:
                self._send_error(400, "Message required")
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
            while self.running:
                self.server.handle_request()
        
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

