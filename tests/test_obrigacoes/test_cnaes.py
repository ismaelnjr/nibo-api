"""
Testes para interface de CNAEs do Nibo Obrigações
"""
import unittest
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestCNAEs(unittest.TestCase):
    """Testes para a interface de CNAEs"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_cnaes(self):
        """Testa listagem de CNAEs"""
        resultado = self.client.cnaes.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)


if __name__ == "__main__":
    unittest.main()

