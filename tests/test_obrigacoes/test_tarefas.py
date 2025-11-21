"""
Testes para interface de tarefas do Nibo Obrigações
"""
import unittest
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestTarefas(unittest.TestCase):
    """Testes para a interface de tarefas"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_tarefas(self):
        """Testa listagem de tarefas"""
        resultado = self.client.tarefas.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)
    
    def test_criar_tarefa(self):
        """Testa criação de tarefa"""
        resultado = self.client.tarefas.criar(
            name="TESTE TAREFA API"
        )
        
        self.assertIn("id", resultado)
        self.assertEqual(resultado["name"], "TESTE TAREFA API")


if __name__ == "__main__":
    unittest.main()

