"""
Main Entry Point - F3-OS Governance Agent
"""

import sys
import argparse
import yaml
from pathlib import Path
from typing import Dict

from .governance_core import GovernanceCore
from .github_integration import GitHubIntegration
from .resource_manager import ResourceManager
from .gui_integration import GUIIntegration, AssistantAPI


def load_config(config_path: Path) -> Dict:
    """Carga configuración desde archivo YAML"""
    if not config_path.exists():
        print(f"Error: Archivo de configuración no encontrado: {config_path}")
        print(f"Por favor, copia config/config.example.yaml a config/config.yaml y configúralo.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def evaluate_pr(pr_number: int, config: Dict, data_dir: Path, dry_run: bool = False):
    """Evalúa un PR específico"""
    print(f"🔍 Evaluando PR #{pr_number}...")
    
    # Inicializar componentes
    governance = GovernanceCore(config, data_dir)
    github = GitHubIntegration(config)
    
    # Obtener datos del PR (con throttling)
    try:
        pr_data = github.get_pr(pr_number, governance.resource_manager)
    except Exception as e:
        print(f"❌ Error obteniendo PR: {e}")
        return
    
    print(f"📄 PR: {pr_data['title']}")
    print(f"👤 Autor: {pr_data['user']}")
    print(f"📁 Archivos: {len(pr_data['files'])}")
    
    # Evaluar
    evaluation = governance.evaluate_pr(pr_data)
    
    # Mostrar resultados
    print("\n" + "="*60)
    print(evaluation['feedback'])
    print("="*60)
    
    decision = evaluation['decision']
    print(f"\n🎯 Decisión: {decision['action'].upper()}")
    print(f"📝 Razón: {decision['reason'][:200]}...")
    
    # Aplicar decisión (si no es dry-run)
    if not dry_run:
        if decision['action'] == 'approve':
            if decision.get('auto', False):
                print("✅ Auto-aprobando PR...")
                github.approve_pr(pr_number, evaluation['feedback'])
            else:
                print("✅ Aprobando PR (requiere revisión humana)...")
                github.comment_on_pr(pr_number, evaluation['feedback'])
        elif decision['action'] == 'request_changes':
            print("🔄 Solicitando cambios...")
            github.request_changes(pr_number, evaluation['feedback'])
        elif decision['action'] == 'reject':
            print("❌ Rechazando PR...")
            github.comment_on_pr(pr_number, evaluation['feedback'])
    else:
        print("\n🔍 DRY RUN - No se aplicaron cambios en GitHub")


def monitor_prs(config: Dict, data_dir: Path, dry_run: bool = False):
    """Monitorea PRs abiertos automáticamente"""
    print("👀 Monitoreando PRs abiertos...")
    
    github = GitHubIntegration(config)
    governance = GovernanceCore(config, data_dir)
    
    pr_numbers = github.get_open_prs()
    print(f"📋 Encontrados {len(pr_numbers)} PRs abiertos")
    
    # Mostrar límites de recursos
    governance.resource_manager.print_resource_stats()
    print()
    
    for pr_number in pr_numbers:
        print(f"\n{'='*60}")
        evaluate_pr(pr_number, config, data_dir, dry_run)
        print(f"{'='*60}\n")
        
        # Mostrar uso de recursos después de cada PR
        governance.resource_manager.print_resource_stats()
        print()


def show_status(config: Dict, data_dir: Path):
    """Muestra estado actual del agente"""
    governance = GovernanceCore(config, data_dir)
    status = governance.get_status()
    
    print("📊 Estado del Agente F3-OS")
    print("="*60)
    print(f"Fase actual: {status['phase'].upper()}")
    print(f"Entropía: {status['entropy']}/255")
    print(f"Perfection Score: {status['perfection_score']}")
    print(f"Ciclos completados: {status['cycle_count']}")
    print("\n" + status['context'])
    
    # Mostrar estadísticas de recursos
    if 'resources' in status:
        governance.resource_manager.print_resource_stats()


def run_cycle(config: Dict, data_dir: Path):
    """Ejecuta un ciclo completo de desarrollo"""
    print("🔄 Ejecutando ciclo de desarrollo...")
    monitor_prs(config, data_dir, dry_run=False)
    show_status(config, data_dir)


def start_gui_server(config: Dict, data_dir: Path, port: int = 8080):
    """Inicia servidor HTTP para GUI del asistente"""
    print(f"🎨 Iniciando servidor GUI del asistente en puerto {port}...")
    
    from .gui_server import GUIServer
    
    governance = GovernanceCore(config, data_dir)
    resource_manager = ResourceManager(config)
    resource_manager.start_monitoring()
    
    from .gui_integration import GUIIntegration
    gui = GUIIntegration(governance, resource_manager, config)
    
    server = GUIServer(gui, port=port)
    server.start()
    
    print(f"✅ Servidor iniciado. GUI puede conectarse a http://localhost:{port}")
    print("Presiona Ctrl+C para detener")
    
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        server.stop()
        resource_manager.stop_monitoring()


def main():
    """Punto de entrada principal"""
    parser = argparse.ArgumentParser(
        description='F3-OS Governance Agent - Agente AI que gobierna el desarrollo de F3-OS'
    )
    
    parser.add_argument(
        'command',
        choices=['evaluate-pr', 'monitor', 'status', 'cycle', 'gui-server'],
        help='Comando a ejecutar'
    )
    
    parser.add_argument(
        '--pr',
        type=int,
        help='Número de PR a evaluar (para evaluate-pr)'
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        default=Path(__file__).parent.parent / 'config' / 'config.yaml',
        help='Ruta al archivo de configuración'
    )
    
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=Path(__file__).parent.parent / 'data',
        help='Directorio para datos persistentes'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Ejecutar sin hacer cambios en GitHub'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Puerto para servidor GUI (para gui-server)'
    )
    
    args = parser.parse_args()
    
    # Cargar configuración
    config = load_config(args.config)
    
    # Crear directorio de datos si no existe
    args.data_dir.mkdir(parents=True, exist_ok=True)
    
    # Ejecutar comando
    if args.command == 'evaluate-pr':
        if not args.pr:
            print("Error: --pr es requerido para evaluate-pr")
            sys.exit(1)
        evaluate_pr(args.pr, config, args.data_dir, args.dry_run)
    
    elif args.command == 'monitor':
        monitor_prs(config, args.data_dir, args.dry_run)
    
    elif args.command == 'status':
        show_status(config, args.data_dir)
    
    elif args.command == 'cycle':
        run_cycle(config, args.data_dir)
    
    elif args.command == 'gui-server':
        start_gui_server(config, args.data_dir, args.port)


if __name__ == '__main__':
    main()

