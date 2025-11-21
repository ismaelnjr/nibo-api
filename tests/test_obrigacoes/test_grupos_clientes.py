"""
Testes para interface de grupos de clientes do Nibo Obrigações
"""
import unittest
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestGruposClientes(unittest.TestCase):
    """Testes para a interface de grupos de clientes"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_grupos_clientes(self):
        """Testa listagem de grupos de clientes"""
        resultado = self.client.grupos_clientes.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)


if __name__ == "__main__":
    unittest.main()

