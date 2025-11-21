"""
Testes para interface de clientes do Nibo Obrigações
"""
import unittest
from uuid import UUID
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestClientes(unittest.TestCase):
    """Testes para a interface de clientes"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_clientes(self):
        """Testa listagem de clientes"""
        resultado = self.client.clientes.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)
    
    def test_criar_cliente(self):
        """Testa criação de cliente"""
        resultado = self.client.clientes.criar(
            name="TESTE CLIENTE OBRIGACOES API"
        )
        
        self.assertIn("id", resultado)
        self.assertEqual(resultado["name"], "TESTE CLIENTE OBRIGACOES API")


if __name__ == "__main__":
    unittest.main()

