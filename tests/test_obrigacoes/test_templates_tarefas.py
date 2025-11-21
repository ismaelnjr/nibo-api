"""
Testes para interface de templates de tarefas do Nibo Obrigações
"""
import unittest
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestTemplatesTarefas(unittest.TestCase):
    """Testes para a interface de templates de tarefas"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_templates_tarefas(self):
        """Testa listagem de templates de tarefas"""
        resultado = self.client.templates_tarefas.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)


if __name__ == "__main__":
    unittest.main()

