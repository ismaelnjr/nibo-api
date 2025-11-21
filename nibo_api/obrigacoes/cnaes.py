"""
Interface para CNAEs no Nibo Obrigações
"""
from typing import Optional, Dict, Any

from nibo_api.common.client import BaseClient


class CNAEsInterface:
    """Interface para operações com CNAEs"""
    
    def __init__(self, client: BaseClient):
        """
        Inicializa a interface de CNAEs
        
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
        Lista todos os CNAEs
        
        Args:
            odata_filter: Filtro OData
            odata_orderby: Campo para ordenação
            odata_top: Limite de registros
            odata_skip: Registros a pular
            
        Returns:
            Dicionário com 'items' (lista de CNAEs) e 'count' (total)
        """
        return self.client.get(
            "/cnaes",
            odata_filter=odata_filter,
            odata_orderby=odata_orderby,
            odata_top=odata_top,
            odata_skip=odata_skip
        )

