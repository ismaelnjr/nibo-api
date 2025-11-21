"""
Cliente principal para a API Nibo Empresa
"""
from typing import Optional
from nibo_api.config import NiboConfig
from nibo_api.common.client import BaseClient
from nibo_api.empresa.contatos.clientes import ClientesInterface
from nibo_api.empresa.contatos.fornecedores import FornecedoresInterface
from nibo_api.empresa.contatos.funcionarios import FuncionariosInterface
from nibo_api.empresa.contatos.socios import SociosInterface
from nibo_api.empresa.categorias import CategoriasInterface
from nibo_api.empresa.centro_custo import CentroCustoInterface
from nibo_api.empresa.empresas import EmpresasInterface
from nibo_api.empresa.agendamentos.receber import AgendamentosReceberInterface
from nibo_api.empresa.agendamentos.pagar import AgendamentosPagarInterface
from nibo_api.empresa.agendamentos.recebimentos import RecebimentosInterface
from nibo_api.empresa.agendamentos.pagamentos import PagamentosInterface
from nibo_api.empresa.agendamentos.arquivos import ArquivosAgendamentoInterface
from nibo_api.empresa.agendamentos.anotacoes import AnotacoesAgendamentoInterface
from nibo_api.empresa.conciliacao import ConciliacaoInterface
from nibo_api.empresa.contas_extratos import ContasExtratosInterface
from nibo_api.empresa.parcelamentos import ParcelamentosInterface
from nibo_api.empresa.arquivos import ArquivosInterface
from nibo_api.empresa.nota_fiscal import NotaFiscalInterface
from nibo_api.empresa.relatorios import RelatoriosInterface
from nibo_api.empresa.cobrancas import CobrancasInterface


class NiboEmpresaClient(BaseClient):
    """Cliente principal para interagir com a API Nibo Empresa"""
    
    def __init__(self, config: Optional[NiboConfig] = None):
        """
        Inicializa o cliente Nibo Empresa
        
        Args:
            config: Instância de NiboConfig. Se None, cria uma nova.
        """
        if config is None:
            config = NiboConfig()
        super().__init__(config, base_url=config.empresa_base_url)
        
        # Inicializa interfaces
        self.clientes = ClientesInterface(self)
        self.fornecedores = FornecedoresInterface(self)
        self.funcionarios = FuncionariosInterface(self)
        self.socios = SociosInterface(self)
        self.categorias = CategoriasInterface(self)
        self.centro_custo = CentroCustoInterface(self)
        self.empresas = EmpresasInterface(self)
        self.agendamentos_receber = AgendamentosReceberInterface(self)
        self.agendamentos_pagar = AgendamentosPagarInterface(self)
        self.recebimentos = RecebimentosInterface(self)
        self.pagamentos = PagamentosInterface(self)
        self.agendamentos_arquivos = ArquivosAgendamentoInterface(self)
        self.agendamentos_anotacoes = AnotacoesAgendamentoInterface(self)
        self.conciliacao = ConciliacaoInterface(self)
        self.contas_extratos = ContasExtratosInterface(self)
        self.parcelamentos = ParcelamentosInterface(self)
        self.arquivos = ArquivosInterface(self)
        self.nota_fiscal = NotaFiscalInterface(self)
        self.relatorios = RelatoriosInterface(self)
        self.cobrancas = CobrancasInterface(self)

