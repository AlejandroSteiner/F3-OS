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
        from pathlib import Path
        
        # Buscar index.html en gui_web/
        script_dir = Path(__file__).parent.parent
        html_path = script_dir / 'gui_web' / 'index.html'
        
        if html_path.exists():
            try:
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
                return
            except Exception as e:
                print(f"Error leyendo HTML: {e}")
        
        # HTML básico si no existe el archivo o hay error
        html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>F3-OS Assistant</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #667eea; }
        .status { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .endpoint { background: #e8f4f8; padding: 10px; margin: 10px 0; border-left: 3px solid #667eea; }
        input, button {
            padding: 10px;
            margin: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button { background: #667eea; color: white; cursor: pointer; }
        button:hover { background: #5568d3; }
        #response { margin-top: 20px; padding: 15px; background: #f9f9f9; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 F3-OS Assistant</h1>
        <p>Servidor GUI del asistente funcionando correctamente.</p>
        
        <div class="status">
            <h3>📊 Estado del Agente</h3>
            <div id="status">Cargando...</div>
        </div>
        
        <h3>💬 Chatear con el Asistente</h3>
        <input type="text" id="query" placeholder="Escribe tu consulta..." style="width: 70%;" />
        <button onclick="sendQuery()">Enviar</button>
        <div id="response"></div>
        
        <h3>🔌 Endpoints API</h3>
        <div class="endpoint">
            <strong>GET /api/status</strong> - Estado del agente
        </div>
        <div class="endpoint">
            <strong>POST /api/query</strong> - Enviar consulta al asistente
        </div>
    </div>
    
    <script>
        // Cargar estado
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                document.getElementById('status').innerHTML = `
                    <p><strong>Fase:</strong> ${data.phase || 'N/A'}</p>
                    <p><strong>Entropía:</strong> ${data.entropy || 0}/255</p>
                    <p><strong>Perfection Score:</strong> ${data.perfection_score || 0}</p>
                    <p><strong>CPU:</strong> ${data.cpu_percent || 0}%</p>
                `;
            })
            .catch(e => document.getElementById('status').textContent = 'Error cargando estado');
        
        // Enviar consulta
        function sendQuery() {
            const query = document.getElementById('query').value;
            if (!query) return;
            
            document.getElementById('response').textContent = 'Pensando...';
            
            fetch('/api/query', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: query})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('response').innerHTML = 
                    '<strong>Asistente:</strong> ' + (data.response || 'Sin respuesta');
                document.getElementById('query').value = '';
            })
            .catch(e => {
                document.getElementById('response').textContent = 'Error: ' + e.message;
            });
        }
        
        // Enter para enviar
        document.getElementById('query').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendQuery();
        });
    </script>
</body>
</html>"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
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
        
        # Intentar iniciar el servidor, si el puerto está ocupado, intentar con otro
        import socket
        original_port = self.port
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                # Verificar si el puerto está disponible
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(1)
                result = test_socket.connect_ex(('localhost', self.port))
                test_socket.close()
                
                if result == 0:
                    # Puerto ocupado, intentar siguiente
                    if attempt < max_attempts - 1:
                        print(f"⚠️  Puerto {self.port} está ocupado, intentando puerto {self.port + 1}...")
                        self.port += 1
                        continue
                    else:
                        raise OSError(f"No se pudo encontrar un puerto disponible después de {max_attempts} intentos")
                
                # Puerto disponible, crear servidor
                self.server = HTTPServer(('localhost', self.port), handler_factory)
                if original_port != self.port:
                    print(f"ℹ️  Usando puerto {self.port} (el puerto {original_port} estaba ocupado)")
                break
                
            except OSError as e:
                if attempt < max_attempts - 1:
                    self.port += 1
                    continue
                else:
                    raise
        
        self.running = True
        
        def run_server():
            print(f"🌐 Servidor GUI del asistente iniciado en http://localhost:{self.port}")
            print(f"📱 Abre en tu navegador: http://localhost:{self.port}")
            print(f"💬 Interfaz web disponible para chatear con el asistente")
            print("")
            self.server.serve_forever()
        
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

