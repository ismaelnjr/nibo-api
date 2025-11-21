"""
Interface para templates de tarefas no Nibo Obrigações
"""
from typing import Optional, Dict, Any

from nibo_api.common.client import BaseClient


class TemplatesTarefasInterface:
    """Interface para operações com templates de tarefas"""
    
    def __init__(self, client: BaseClient):
        """
        Inicializa a interface de templates de tarefas
        
        Args:
            client: Instância do cliente HTTP base
        """
        self.client = client
    
    def listar(
        self,
        odata_filter: Optional[str] = None,
        odata_orderby: Optional[str] = None,
        odata_top: Optional[int] = None,
        odata_skip: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Lista todos os templates de tarefas
        
        Args:
            odata_filter: Filtro OData
            odata_orderby: Campo para ordenação
            odata_top: Limite de registros
            odata_skip: Registros a pular
            
        Returns:
            Dicionário com 'items' (lista de templates) e 'count' (total)
        """
        return self.client.get(
            "/task-templates",
            odata_filter=odata_filter,
            odata_orderby=odata_orderby,
            odata_top=odata_top,
            odata_skip=odata_skip
        )

