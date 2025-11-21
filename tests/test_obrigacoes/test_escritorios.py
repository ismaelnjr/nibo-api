"""
Testes para interface de escritórios do Nibo Obrigações
"""
import unittest
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestEscritorios(unittest.TestCase):
    """Testes para a interface de escritórios"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_escritorios(self):
        """Testa listagem de escritórios"""
        resultado = self.client.escritorios.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)


if __name__ == "__main__":
    unittest.main()

