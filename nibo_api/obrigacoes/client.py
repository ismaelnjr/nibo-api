"""
Cliente principal para a API Nibo Obrigações
"""
from typing import Optional
from nibo_api.config import NiboConfig
from nibo_api.common.client import BaseClient
from nibo_api.obrigacoes.escritorios import EscritoriosInterface
from nibo_api.obrigacoes.usuarios import UsuariosInterface
from nibo_api.obrigacoes.arquivos import ArquivosInterface
from nibo_api.obrigacoes.conferencia import ConferenciaInterface
from nibo_api.obrigacoes.contatos import ContatosInterface
from nibo_api.obrigacoes.clientes import ClientesInterface
from nibo_api.obrigacoes.cnaes import CNAEsInterface
from nibo_api.obrigacoes.grupos_clientes import GruposClientesInterface
from nibo_api.obrigacoes.departamentos import DepartamentosInterface
from nibo_api.obrigacoes.tarefas import TarefasInterface
from nibo_api.obrigacoes.templates_tarefas import TemplatesTarefasInterface
from nibo_api.obrigacoes.responsabilidades import ResponsabilidadesInterface
from nibo_api.obrigacoes.relatorios import RelatoriosInterface


class NiboObrigacoesClient(BaseClient):
    """Cliente principal para interagir com a API Nibo Obrigações"""
    
    def __init__(self, config: Optional[NiboConfig] = None):
        """
        Inicializa o cliente Nibo Obrigações
        
        Args:
            config: Instância de NiboConfig. Se None, cria uma nova.
        """
        if config is None:
            config = NiboConfig()
        super().__init__(config, base_url=config.obrigacoes_base_url)
        
        # Inicializa interfaces
        self.escritorios = EscritoriosInterface(self)
        self.usuarios = UsuariosInterface(self)
        self.arquivos = ArquivosInterface(self)
        self.conferencia = ConferenciaInterface(self)
        self.contatos = ContatosInterface(self)
        self.clientes = ClientesInterface(self)
        self.cnaes = CNAEsInterface(self)
        self.grupos_clientes = GruposClientesInterface(self)
        self.departamentos = DepartamentosInterface(self)
        self.tarefas = TarefasInterface(self)
        self.templates_tarefas = TemplatesTarefasInterface(self)
        self.responsabilidades = ResponsabilidadesInterface(self)
        self.relatorios = RelatoriosInterface(self)

