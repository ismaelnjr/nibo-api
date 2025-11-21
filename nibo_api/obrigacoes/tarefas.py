"""
Interface para tarefas no Nibo Obrigações
"""
from typing import Optional, Dict, Any
from uuid import UUID

from nibo_api.common.client import BaseClient


class TarefasInterface:
    """Interface para operações com tarefas"""
    
    def __init__(self, client: BaseClient):
        """
        Inicializa a interface de tarefas
        
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
        Lista todas as tarefas
        
        Args:
            odata_filter: Filtro OData
            odata_orderby: Campo para ordenação
            odata_top: Limite de registros
            odata_skip: Registros a pular
            
        Returns:
            Dicionário com 'items' (lista de tarefas) e 'count' (total)
        """
        return self.client.get(
            "/tasks",
            odata_filter=odata_filter,
            odata_orderby=odata_orderby,
            odata_top=odata_top,
            odata_skip=odata_skip
        )
    
    def criar(
        self,
        name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Cria uma nova tarefa
        
        Args:
            name: Nome da tarefa
            **kwargs: Outros campos opcionais
            
        Returns:
            Dados da tarefa criada
        """
        payload = {
            "name": name
        }
        payload.update(kwargs)
        
        return self.client.post("/tasks", json_data=payload)

