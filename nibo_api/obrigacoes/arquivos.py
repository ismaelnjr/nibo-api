"""
Interface para arquivos no Nibo Obrigações
"""
from typing import Optional, Dict, Any

from nibo_api.common.client import BaseClient


class ArquivosInterface:
    """Interface para operações com arquivos"""
    
    def __init__(self, client: BaseClient):
        """
        Inicializa a interface de arquivos
        
        Args:
            client: Instância do cliente HTTP base
        """
        self.client = client
    
    def criar_arquivo_upload(
        self,
        name: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Cria arquivo para upload
        
        Args:
            name: Nome do arquivo
            **kwargs: Outros campos opcionais
            
        Returns:
            Dados do arquivo criado
        """
        payload = {
            "name": name
        }
        payload.update(kwargs)
        
        return self.client.post("/files", json_data=payload)

