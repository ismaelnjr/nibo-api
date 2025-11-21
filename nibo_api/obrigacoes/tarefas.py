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
        accounting_firm_id: UUID,
        odata_filter: Optional[str] = None,
        odata_orderby: Optional[str] = None,
        odata_top: Optional[int] = None,
        odata_skip: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Lista todas as tarefas de um escritório
        
        Args:
            accounting_firm_id: UUID do escritório contábil
            odata_filter: Filtro OData
            odata_orderby: Campo para ordenação
            odata_top: Limite de registros
            odata_skip: Registros a pular
            
        Returns:
            Dicionário com 'items' (lista de tarefas) e 'metadata'
        """
        return self.client.get(
            f"/accountingfirms/{accounting_firm_id}/tasks",
            odata_filter=odata_filter,
            odata_orderby=odata_orderby,
            odata_top=odata_top,
            odata_skip=odata_skip
        )
    
    def criar(
        self,
        accounting_firm_id: UUID,
        name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Cria uma nova tarefa
        
        Args:
            accounting_firm_id: UUID do escritório contábil
            name: Nome da tarefa
            **kwargs: Outros campos opcionais
            
        Returns:
            Dados da tarefa criada
        """
        payload = {
            "name": name
        }
        payload.update(kwargs)
        
        return self.client.post(
            f"/accountingfirms/{accounting_firm_id}/tasks",
            json_data=payload
        )

