"""
Interface para recebimentos (contas recebidas) no Nibo Empresa
"""
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

from nibo_api.common.client import BaseClient


class RecebimentosInterface:
    """Interface para operações com recebimentos (contas recebidas)"""
    
    def __init__(self, client: BaseClient):
        """
        Inicializa a interface de recebimentos
        
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
        Lista recebimentos (contas recebidas)
        
        Args:
            odata_filter: Filtro OData
            odata_orderby: Campo para ordenação
            odata_top: Limite de registros
            odata_skip: Registros a pular
            
        Returns:
            Dicionário com 'items' (lista de recebimentos) e 'count' (total)
        """
        return self.client.get(
            "/receipts",
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
        Lista recebimentos realizados no período informado.

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
        Cria um novo recebimento
        
        Args:
            categories: Lista de categorias com categoryId, value e description
            stakeholder_id: UUID do stakeholder (cliente)
            payment_date: Data do pagamento (formato: DD/MM/YYYY)
            description: Descrição do recebimento
            reference: Referência do recebimento (opcional)
            **kwargs: Outros campos opcionais
            
        Returns:
            Dados do recebimento criado
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
        
        return self.client.post("/receipts", json_data=payload)
    
    def criar_json(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um recebimento usando payload JSON completo
        
        Args:
            payload: Dicionário completo com dados do recebimento
            
        Returns:
            Dados do recebimento criado
        """
        return self.client.post("/receipts", json_data=payload)
    
    def excluir(self, entry_id: UUID) -> Dict[str, Any]:
        """
        Exclui um recebimento
        
        Args:
            entry_id: UUID do recebimento
            
        Returns:
            Resposta da API
        """
        return self.client.delete(f"/receipts/{entry_id}")

