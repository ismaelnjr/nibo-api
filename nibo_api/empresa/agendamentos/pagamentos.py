"""
Interface para pagamentos (contas pagas) no Nibo Empresa
"""
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from nibo_api.common.client import BaseClient


class PagamentosInterface:
    """Interface para operações com pagamentos (contas pagas)"""
    
    def __init__(self, client: BaseClient):
        """
        Inicializa a interface de pagamentos
        
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
        Lista pagamentos (contas pagas)
        
        Args:
            odata_filter: Filtro OData
            odata_orderby: Campo para ordenação
            odata_top: Limite de registros
            odata_skip: Registros a pular
            
        Returns:
            Dicionário com 'items' (lista de pagamentos) e 'count' (total)
        """
        return self.client.get(
            "/payments",
            odata_filter=odata_filter,
            odata_orderby=odata_orderby,
            odata_top=odata_top,
            odata_skip=odata_skip
        )

    def listar_por_periodo(
        self,
        data_inicio: str,
        data_fim: str,
        odata_orderby: str = "date desc",
        odata_top: Optional[int] = None,
        odata_skip: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Lista pagamentos realizados no período informado.

        Aceita data em DD/MM/YYYY ou YYYY-MM-DD.
        """
        inicio = self._parse_data(data_inicio)
        fim = self._parse_data(data_fim)
        if not inicio or not fim:
            raise ValueError("Datas inválidas. Use DD/MM/YYYY ou YYYY-MM-DD.")
        if inicio > fim:
            raise ValueError("Data inicial não pode ser maior que data final.")

        filtro = (
            f"date ge {inicio.strftime('%Y-%m-%dT00:00:00Z')} "
            f"and date le {fim.strftime('%Y-%m-%dT23:59:59Z')}"
        )
        return self.listar(
            odata_filter=filtro,
            odata_orderby=odata_orderby,
            odata_top=odata_top,
            odata_skip=odata_skip
        )

    @staticmethod
    def _parse_data(data_str: str):
        if not data_str:
            return None
        valor = data_str.strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(valor, fmt)
            except ValueError:
                continue
        return None
    
    def criar(
        self,
        categories: list,
        stakeholder_id: UUID,
        payment_date: str,
        description: str,
        reference: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Cria um novo pagamento
        
        Args:
            categories: Lista de categorias com categoryId, value e description
            stakeholder_id: UUID do stakeholder (fornecedor)
            payment_date: Data do pagamento (formato: DD/MM/YYYY)
            description: Descrição do pagamento
            reference: Referência do pagamento (opcional)
            **kwargs: Outros campos opcionais
            
        Returns:
            Dados do pagamento criado
        """
        payload = {
            "categories": categories,
            "stakeholderId": str(stakeholder_id),
            "paymentDate": payment_date,
            "description": description
        }
        
        if reference:
            payload["reference"] = reference
        
        payload.update(kwargs)
        
        return self.client.post("/payments", json_data=payload)
    
    def criar_json(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um pagamento usando payload JSON completo
        
        Args:
            payload: Dicionário completo com dados do pagamento
            
        Returns:
            Dados do pagamento criado
        """
        return self.client.post("/payments", json_data=payload)
    
    def excluir(self, entry_id: UUID) -> Dict[str, Any]:
        """
        Exclui um pagamento
        
        Args:
            entry_id: UUID do pagamento
            
        Returns:
            Resposta da API
        """
        return self.client.delete(f"/payments/{entry_id}")

