"""
Sistema de configuração para a API Nibo
"""
import json
import os
from pathlib import Path
from typing import Optional


class NiboConfig:
    """Gerencia as configurações da API Nibo"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa a configuração
        
        Args:
            config_path: Caminho para o arquivo config.json. Se None, tenta encontrar
                        automaticamente na raiz do projeto.
        """
        if config_path is None:
            # Tenta encontrar config.json na raiz do projeto
            current_dir = Path(__file__).parent.parent
            config_path = current_dir / "config.json"
        
        self.config_path = Path(config_path)
        self._config = self._load_config()
    
    def _load_config(self) -> dict:
        """Carrega configuração do arquivo JSON ou cria um dicionário vazio"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                raise ValueError(f"Erro ao carregar config.json: {e}")
        return {}
    
    @property
    def api_token(self) -> str:
        """
        Token de API do Nibo Empresa (padrão)
        
        Returns:
            Token de API (prioridade: variável de ambiente > config.json)
        """
        token = os.getenv("NIBO_API_TOKEN") or self._config.get("api_token")
        if not token:
            raise ValueError(
                "Token de API não encontrado. Configure NIBO_API_TOKEN como "
                "variável de ambiente ou adicione 'api_token' em config.json"
            )
        return token
    
    @property
    def obrigacoes_api_token(self) -> str:
        """
        Token de API do Nibo Obrigações
        
        Returns:
            Token de API de Obrigações (prioridade: variável de ambiente > config.json > api_token padrão)
        """
        token = (
            os.getenv("NIBO_OBRIGACOES_API_TOKEN") 
            or self._config.get("obrigacoes_api_token")
            or self.api_token  # Fallback para token padrão se não especificado
        )
        if not token:
            raise ValueError(
                "Token de API de Obrigações não encontrado."
            )
        return token
    
    @property
    def empresa_base_url(self) -> str:
        """
        URL base da API Nibo Empresa
        
        Returns:
            URL base (padrão: https://api.nibo.com.br/empresas/v1)
        """
        return (
            os.getenv("NIBO_EMPRESA_BASE_URL") 
            or self._config.get("empresa_base_url")
            or "https://api.nibo.com.br/empresas/v1"
        )
    
    @property
    def obrigacoes_base_url(self) -> str:
        """
        URL base da API Nibo Obrigações
        
        Returns:
            URL base (padrão: https://api.nibo.com.br/accountant/api/v1)
        """
        return (
            os.getenv("NIBO_OBRIGACOES_BASE_URL")
            or self._config.get("obrigacoes_base_url")
            or "https://api.nibo.com.br/accountant/api/v1"
        )
    
    @property
    def obrigacoes_user_id(self) -> Optional[str]:
        """
        User ID para API Nibo Obrigações (opcional, necessário se token não estiver vinculado a usuário)
        
        Returns:
            User ID (prioridade: variável de ambiente > config.json)
        """
        return (
            os.getenv("NIBO_OBRIGACOES_USER_ID")
            or self._config.get("obrigacoes_user_id")
        )
    
    def save_config(self, config: dict):
        """
        Salva configuração no arquivo config.json
        
        Args:
            config: Dicionário com as configurações
        """
        self._config.update(config)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

