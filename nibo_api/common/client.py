"""
Cliente HTTP base para comunicação com a API Nibo
"""
import requests
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode

from nibo_api.config import NiboConfig
from nibo_api.common.exceptions import (
    NiboAPIError,
    NiboAuthenticationError,
    NiboNotFoundError,
    NiboValidationError,
    NiboServerError,
    NiboRateLimitError
)


class BaseClient:
    """Cliente HTTP base com autenticação e suporte a OData"""
    
    def __init__(self, config: Optional[NiboConfig] = None, base_url: str = ""):
        """
        Inicializa o cliente base
        
        Args:
            config: Instância de NiboConfig. Se None, cria uma nova.
            base_url: URL base da API
        """
        self.config = config or NiboConfig()
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "ApiToken": self.config.api_token
        })
    
    def _handle_response(self, response: requests.Response) -> Any:
        """
        Trata a resposta HTTP e lança exceções apropriadas
        
        Args:
            response: Resposta HTTP
            
        Returns:
            Dados JSON da resposta
            
        Raises:
            NiboAuthenticationError: Erro 401
            NiboNotFoundError: Erro 404
            NiboValidationError: Erro 400
            NiboRateLimitError: Erro 429
            NiboServerError: Erros 5xx
            NiboAPIError: Outros erros
        """
        if response.status_code == 200 or response.status_code == 201:
            try:
                return response.json()
            except ValueError:
                return response.text
        
        elif response.status_code == 401:
            raise NiboAuthenticationError(
                f"Erro de autenticação: {response.text}"
            )
        elif response.status_code == 404:
            raise NiboNotFoundError(
                f"Recurso não encontrado: {response.text}"
            )
        elif response.status_code == 400:
            raise NiboValidationError(
                f"Erro de validação: {response.text}"
            )
        elif response.status_code == 429:
            raise NiboRateLimitError(
                f"Limite de requisições excedido: {response.text}"
            )
        elif 500 <= response.status_code < 600:
            raise NiboServerError(
                f"Erro do servidor ({response.status_code}): {response.text}"
            )
        else:
            raise NiboAPIError(
                f"Erro na requisição ({response.status_code}): {response.text}"
            )
    
    def _build_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Constrói URL completa com parâmetros
        
        Args:
            endpoint: Endpoint da API (ex: "/customers")
            params: Parâmetros de query string
            
        Returns:
            URL completa
        """
        url = f"{self.base_url}{endpoint}"
        if params:
            # Remove valores None
            params = {k: v for k, v in params.items() if v is not None}
            if params:
                url += f"?{urlencode(params)}"
        return url
    
    def get(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        odata_filter: Optional[str] = None,
        odata_orderby: Optional[str] = None,
        odata_top: Optional[int] = None,
        odata_skip: Optional[int] = None
    ) -> Any:
        """
        Realiza requisição GET
        
        Args:
            endpoint: Endpoint da API
            params: Parâmetros adicionais de query string
            odata_filter: Filtro OData ($filter)
            odata_orderby: Ordenação OData ($orderby)
            odata_top: Limite de registros ($top)
            odata_skip: Registros a pular ($skip)
            
        Returns:
            Resposta JSON da API
        """
        query_params = params or {}
        
        # Adiciona parâmetros OData
        if odata_filter:
            query_params["$filter"] = odata_filter
        if odata_orderby:
            query_params["$orderby"] = odata_orderby
        if odata_top is not None:
            query_params["$top"] = odata_top
        if odata_skip is not None:
            query_params["$skip"] = odata_skip
        
        url = self._build_url(endpoint, query_params)
        response = self.session.get(url)
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Realiza requisição POST
        
        Args:
            endpoint: Endpoint da API
            data: Dados a enviar (form-data)
            json_data: Dados JSON a enviar
            
        Returns:
            Resposta JSON da API
        """
        url = self._build_url(endpoint)
        response = self.session.post(url, data=data, json=json_data)
        return self._handle_response(response)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None) -> Any:
        """
        Realiza requisição PUT
        
        Args:
            endpoint: Endpoint da API
            data: Dados a enviar (form-data)
            json_data: Dados JSON a enviar
            
        Returns:
            Resposta JSON da API
        """
        url = self._build_url(endpoint)
        response = self.session.put(url, data=data, json=json_data)
        return self._handle_response(response)
    
    def delete(self, endpoint: str) -> Any:
        """
        Realiza requisição DELETE
        
        Args:
            endpoint: Endpoint da API
            
        Returns:
            Resposta da API
        """
        url = self._build_url(endpoint)
        response = self.session.delete(url)
        return self._handle_response(response)

