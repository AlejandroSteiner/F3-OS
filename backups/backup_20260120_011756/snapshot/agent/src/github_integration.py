"""
GitHub Integration - Interfaz con GitHub API
"""

from github import Github
from typing import Dict, List, Optional
import base64


class GitHubIntegration:
    """Integración con GitHub API"""
    
    def __init__(self, config: dict):
        self.config = config
        github_config = config.get('github', {})
        self.token = github_config.get('token')
        self.owner = github_config.get('owner')
        self.repo_name = github_config.get('repo')
        self.main_branch = github_config.get('main_branch', 'main')
        
        if not self.token:
            raise ValueError("GitHub token no configurado")
        
        self.github = Github(self.token)
        self.repo = self.github.get_repo(f"{self.owner}/{self.repo_name}")
    
    def get_pr(self, pr_number: int, resource_manager=None) -> Dict:
        """Obtiene datos de un PR"""
        # Aplicar throttling si se proporciona resource_manager
        if resource_manager:
            from .resource_manager import ThrottledOperation
            with ThrottledOperation(resource_manager):
                pr = self.repo.get_pull(pr_number)
        else:
            pr = self.repo.get_pull(pr_number)
        
        # Obtener archivos cambiados
        files = []
        for file in pr.get_files():
            files.append({
                'filename': file.filename,
                'status': file.status,
                'additions': file.additions,
                'deletions': file.deletions,
                'changes': file.changes,
            })
        
        # Obtener diff
        diff = pr.diff
        
        # Obtener información del PR
        pr_data = {
            'number': pr.number,
            'title': pr.title,
            'body': pr.body or '',
            'state': pr.state,
            'user': pr.user.login,
            'created_at': pr.created_at.isoformat(),
            'updated_at': pr.updated_at.isoformat(),
            'files': files,
            'diff': diff,
            'labels': [label.name for label in pr.labels],
            'draft': pr.draft,
            'mergeable': pr.mergeable,
        }
        
        return pr_data
    
    def get_open_prs(self) -> List[int]:
        """Obtiene lista de PRs abiertos"""
        prs = self.repo.get_pulls(state='open', sort='created', direction='desc')
        return [pr.number for pr in prs]
    
    def comment_on_pr(self, pr_number: int, comment: str) -> None:
        """Comenta en un PR"""
        pr = self.repo.get_pull(pr_number)
        pr.create_issue_comment(comment)
    
    def approve_pr(self, pr_number: int, comment: Optional[str] = None) -> None:
        """Aprueba un PR (requiere permisos de review)"""
        pr = self.repo.get_pull(pr_number)
        if comment:
            pr.create_review(body=comment, event='APPROVE')
        else:
            pr.create_review(event='APPROVE')
    
    def request_changes(self, pr_number: int, comment: str) -> None:
        """Solicita cambios en un PR"""
        pr = self.repo.get_pull(pr_number)
        pr.create_review(body=comment, event='REQUEST_CHANGES')
    
    def reject_pr(self, pr_number: int, comment: str) -> None:
        """Rechaza un PR (comentando y cerrando)"""
        self.comment_on_pr(pr_number, comment)
        pr = self.repo.get_pull(pr_number)
        pr.edit(state='closed')
    
    def get_related_issues(self, pr_number: int) -> List[Dict]:
        """Obtiene Issues relacionados con el PR"""
        pr = self.repo.get_pull(pr_number)
        # Buscar Issues mencionados en el body o commits
        # Esto es una implementación básica
        issues = []
        
        if pr.body:
            # Buscar referencias a Issues (#123)
            import re
            issue_refs = re.findall(r'#(\d+)', pr.body)
            for ref in issue_refs:
                try:
                    issue = self.repo.get_issue(int(ref))
                    issues.append({
                        'number': issue.number,
                        'title': issue.title,
                        'labels': [label.name for label in issue.labels],
                        'state': issue.state,
                    })
                except:
                    pass
        
        return issues
    
    def check_conceptual_issue(self, pr_number: int) -> bool:
        """Verifica si hay un Issue [CONCEPTUAL] relacionado"""
        issues = self.get_related_issues(pr_number)
        for issue in issues:
            if 'conceptual' in [l.lower() for l in issue.get('labels', [])]:
                return True
        return False

