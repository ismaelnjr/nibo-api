"""
Testes para interface de contatos do Nibo Obrigações
"""
import unittest
from uuid import UUID
from nibo_api.config import NiboConfig
from nibo_api.obrigacoes.client import NiboObrigacoesClient


class TestContatos(unittest.TestCase):
    """Testes para a interface de contatos"""
    
    def setUp(self):
        """Configuração inicial dos testes"""
        self.config = NiboConfig()
        self.client = NiboObrigacoesClient(self.config)
    
    def test_listar_contatos(self):
        """Testa listagem de contatos"""
        resultado = self.client.contatos.listar()
        
        self.assertIn("items", resultado)
        self.assertIn("count", resultado)
        self.assertIsInstance(resultado["items"], list)
        self.assertIsInstance(resultado["count"], int)
    
    def test_buscar_contato_por_id(self):
        """Testa busca de contato por ID"""
        # Primeiro lista contatos para pegar um ID válido
        contatos = self.client.contatos.listar(odata_top=1)
        
        if contatos["items"]:
            contato_id = UUID(contatos["items"][0]["id"])
            resultado = self.client.contatos.buscar_por_id(contato_id)
            
            self.assertIn("id", resultado)
            self.assertEqual(str(resultado["id"]), str(contato_id))
    
    def test_listar_departamentos(self):
        """Testa listagem de departamentos de um contato"""
        # Primeiro lista contatos para pegar um ID válido
        contatos = self.client.contatos.listar(odata_top=1)
        
        if contatos["items"]:
            contato_id = UUID(contatos["items"][0]["id"])
            resultado = self.client.contatos.listar_departamentos(contato_id)
            
            self.assertIsInstance(resultado, (dict, list))


if __name__ == "__main__":
    unittest.main()

