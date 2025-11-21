"""
Testes para interface de departamentos do Nibo Obrigações
"""
import unittest
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestDepartamentos(unittest.TestCase):
    """Testes para a interface de departamentos"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_departamentos(self):
        """Testa listagem de departamentos"""
        resultado = self.client.departamentos.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)


if __name__ == "__main__":
    unittest.main()

